"""Acceptance tests for ai-meta-repo-template.

Run from the repository root:
    python -m unittest discover -s tests -v
Regenerate golden snapshots after an intended change, then review the diff:
    UPDATE_GOLDEN=1 python -m unittest discover -s tests

Requirements: Python 3.9+, git, and Copier 9.19.x on PATH (or COPIER="uvx --from copier==9.19.1 copier").
The tests snapshot the working tree into a temporary git repository tagged v9.9.9 so that rendering
is deterministic and needs no network.
"""

import hashlib
import importlib.util
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"
GOLDEN = ROOT / "tests" / "golden"
COPIER = shlex.split(os.environ.get("COPIER", "copier"))
TAG = "v9.9.9"
GIT_ENV = {
    "GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
    "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "test@example.invalid",
}
FIXTURE_NAMES = sorted(p.stem for p in FIXTURES.glob("*.yml"))


def run(cmd, cwd=None, check=True):
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8", **GIT_ENV)
    env.pop("GITHUB_REPOSITORY", None)  # folder name, not CI repo name, is checked in tests
    result = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
    if check and result.returncode != 0:
        raise AssertionError("command failed: %s\n%s\n%s" % (cmd, result.stdout, result.stderr))
    return result


def write(path, text, encoding="utf-8"):
    """Write text with LF line endings on every platform (Path.write_text translates on Windows)."""
    with open(str(path), "w", encoding=encoding, newline="\n") as handle:
        handle.write(text)


def git(cwd, *args, check=True):
    return run(["git", *args], cwd=cwd, check=check)


def commit_all(cwd, message):
    git(cwd, "add", "-A")
    git(cwd, "commit", "-q", "--allow-empty", "-m", message)


def tree_digest(root):
    """Map of relative path -> sha256 for every file outside .git, with the template path normalized."""
    out = {}
    for path in sorted(Path(root).rglob("*")):
        if ".git" in path.relative_to(root).parts or not path.is_file():
            continue
        data = path.read_bytes().replace(b"\r\n", b"\n")
        if path.name == ".copier-answers.yml":
            data = re.sub(rb"(?m)^_src_path: .*$", b"_src_path: <template>", data)
        out[path.relative_to(root).as_posix()] = hashlib.sha256(data).hexdigest()
    return out


class TemplateTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # resolve(): Windows runners expose TEMP as an 8.3 short path, which copier update rejects.
        cls.tmp = Path(tempfile.mkdtemp(prefix="tpl-test-")).resolve()
        cls.template = cls.tmp / "template-src"
        cls.template.mkdir()
        files = git(ROOT, "ls-files", "-co", "--exclude-standard", "-z").stdout.split("\0")
        for rel in filter(None, files):
            src = ROOT / rel
            if src.is_file():
                dst = cls.template / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
        git(cls.template, "init", "-q", "-b", "main")
        commit_all(cls.template, "snapshot")
        git(cls.template, "tag", TAG)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    # --- helpers -------------------------------------------------------------

    def copy(self, fixture, dest_parent=None, extra=(), ref=TAG):
        project_id = fixture
        dest = Path(dest_parent or tempfile.mkdtemp(dir=str(self.tmp))).resolve() / project_id
        run(COPIER + ["copy", "--defaults", "--quiet", "--vcs-ref", ref,
                      "--data-file", str(FIXTURES / (fixture + ".yml")), *extra,
                      str(self.template), str(dest)])
        return dest

    def init_repo(self, dest):
        git(dest, "init", "-q", "-b", "main")
        commit_all(dest, "chore: initialize from ai-meta-repo-template")

    def validate(self, dest, *args):
        result = run([sys.executable, str(dest / "scripts" / "check_governance.py"), *args], check=False)
        return result.returncode, result.stdout

    def assert_valid(self, dest):
        code, out = self.validate(dest)
        self.assertEqual(code, 0, out)
        return out

    def update(self, dest, *args):
        return run(COPIER + ["update", "--defaults", "--quiet", "--conflict", "rej", *args], cwd=dest)

    def sections(self, dest):
        text = (dest / "AGENTS.md").read_text(encoding="utf-8")
        parts = re.split(r"(?m)^(?=#+ .*<!-- (?:template-owned id=[a-z-]+|project-owned[^>]*) -->)", text)
        result = {}
        for part in parts:
            m = re.match(r"^#+ .*<!-- (?:template-owned id=([a-z-]+)|(project-owned)[^>]*) -->", part)
            if m:
                result[m.group(1) or "project"] = part
        return result

    def load_validator(self, dest):
        spec = importlib.util.spec_from_file_location("check_governance", dest / "scripts" / "check_governance.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


class TestGeneration(TemplateTestCase):
    def test_all_fixtures_render_and_validate(self):
        """All three profiles, public and -private, render and pass the governance check."""
        for fixture in FIXTURE_NAMES:
            with self.subTest(fixture=fixture):
                dest = self.copy(fixture)
                out = self.assert_valid(dest)
                self.assertNotIn("ERROR", out)
                lines = (dest / "AGENTS.md").read_text(encoding="utf-8").count("\n")
                self.assertLessEqual(lines, 200, "AGENTS.md review threshold exceeded")

    def test_golden_snapshots(self):
        """Rendered output matches reviewed snapshots (set UPDATE_GOLDEN=1 to regenerate)."""
        for fixture in FIXTURE_NAMES:
            with self.subTest(fixture=fixture):
                dest = self.copy(fixture)
                digest = tree_digest(dest)
                listing = "".join("%s  %s\n" % (h, p) for p, h in sorted(digest.items()))
                snapshot = {
                    "FILES.txt": listing,
                    "AGENTS.md": (dest / "AGENTS.md").read_text(encoding="utf-8"),
                    "pull_request_template.md": (dest / ".github/pull_request_template.md").read_text(encoding="utf-8"),
                }
                target = GOLDEN / fixture
                if os.environ.get("UPDATE_GOLDEN"):
                    target.mkdir(parents=True, exist_ok=True)
                    for name, content in snapshot.items():
                        write((target / name), content)
                for name, content in snapshot.items():
                    expected = (target / name).read_text(encoding="utf-8").replace("\r\n", "\n")
                    self.assertEqual(content.replace("\r\n", "\n"), expected, "%s/%s changed" % (fixture, name))

    def test_deterministic(self):
        """Equivalent inputs and template revision produce identical trees."""
        fixture = "ai-biz-example-multi-agent"
        self.assertEqual(tree_digest(self.copy(fixture)), tree_digest(self.copy(fixture)))

    def test_template_maintenance_files_not_rendered(self):
        dest = self.copy("ai-biz-example-assisted")
        for rel in ("copier.yml", "includes", "tests", "docs/standard-naming-project.md",
                    "docs/procedure-provisioning.md", "docs/decisions/0001-adopt-copier.md"):
            self.assertFalse((dest / rel).exists(), rel)
        self.assertEqual((dest / "CLAUDE.md").read_text(encoding="utf-8").strip(), "@AGENTS.md")

    def test_private_requirements(self):
        dest = self.copy("ai-home-example-agentic-private")
        self.assertIn("data/", (dest / ".gitignore").read_text(encoding="utf-8").split("\n"))
        self.assertIn("cmn-data-handling", self.sections(dest))
        agents = (dest / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("`perf`", agents)  # extra_types reach the source-control rules
        public = self.copy("ai-biz-example-agentic")
        self.assertNotIn("data/", (public / ".gitignore").read_text(encoding="utf-8").split("\n"))
        self.assertNotIn("cmn-data-handling", self.sections(public))


class TestInheritance(TemplateTestCase):
    def test_layers_per_profile(self):
        """Common everywhere; assisted and agentic exclusive; multi-agent adds to agentic."""
        allowed = {"assisted": {"cmn", "ast"}, "agentic": {"cmn", "agt"}, "multi-agent": {"cmn", "agt", "mag"}}
        rendered = {p: self.sections(self.copy("ai-biz-example-" + p)) for p in allowed}
        for profile, sections in rendered.items():
            layers = {sid.split("-")[0] for sid in sections if sid != "project"}
            self.assertEqual(layers, allowed[profile], profile)
        agentic, multi = rendered["agentic"], rendered["multi-agent"]
        for sid, body in agentic.items():
            if sid.startswith("agt-"):
                self.assertEqual(body, multi[sid], "multi-agent must reuse %s unchanged" % sid)
        for sid in rendered["assisted"]:
            if sid.startswith("cmn-") and sid not in ("cmn-header", "cmn-references", "cmn-modules"):
                self.assertEqual(rendered["assisted"][sid], agentic[sid], sid)
                self.assertEqual(rendered["assisted"][sid], multi[sid], sid)

    def test_no_contradicting_autonomy(self):
        """Each repository gets exactly one autonomy section and no foreign approval model."""
        for profile in ("assisted", "agentic", "multi-agent"):
            text = (self.copy("ai-biz-example-" + profile) / "AGENTS.md").read_text(encoding="utf-8")
            self.assertEqual(len(re.findall(r"^## Autonomy", text, re.M)), 1, profile)
            has_collaborator_rule = "not autonomous agents" in text
            self.assertEqual(has_collaborator_rule, profile == "assisted", profile)
            self.assertEqual("active delegation" in text, profile != "assisted", profile)

    def test_no_duplicate_rules(self):
        for fixture in FIXTURE_NAMES:
            text = (self.copy(fixture) / "AGENTS.md").read_text(encoding="utf-8")
            items = [m.strip() for m in re.findall(r"(?m)^\s*(?:[-*]|\d+\.)\s+(.{25,})$", text)]
            self.assertEqual(len(items), len(set(items)), fixture)


class TestValidator(TemplateTestCase):
    def test_project_id_parity_with_copier(self):
        """The Python validator and the copier.yml validator accept and reject the same IDs."""
        dest = self.copy("ai-biz-example-assisted")
        checker = self.load_validator(dest)
        cases = ["ai-biz-example-shop", "ai-example", "ai-am-printer-profiles-private",
                 "ai-home-example-api-private", "biz-example", "ai-hm-example", "ai-private-example",
                 "ai-example-private-api", "ai-biz-shop-v2", "ai-biz", "AI-Example", "ai--x", "ai-biz-private"]
        for project_id in cases:
            with self.subTest(project_id=project_id):
                py_ok = checker.project_id_error(project_id) is None
                result = run(COPIER + ["copy", "--defaults", "--quiet", "--pretend", "--vcs-ref", TAG,
                                       "--data-file", str(FIXTURES / "ai-biz-example-assisted.yml"),
                                       "--data", "project_id=" + project_id,
                                       "--data", "visibility=private",
                                       "--data", "sensitive_data=x", "--data", "tracked_content=y",
                                       str(self.template), str(self.tmp / "pretend")], check=False)
                self.assertEqual(result.returncode == 0, py_ok, result.stderr[-400:])

    def test_domains_match_standard(self):
        table = (ROOT / "docs/standard-naming-project.md").read_text(encoding="utf-8")
        section = table.split("## 5.")[1].split("\n## ")[0]
        documented = re.findall(r"(?m)^\| `([a-z]+)-` \|", section)
        copier_yml = (ROOT / "copier.yml").read_text(encoding="utf-8")
        configured = re.search(r"(?ms)^domains:.*?default: \[([^\]]*)\]", copier_yml).group(1)
        self.assertEqual(sorted(documented), sorted(d.strip() for d in configured.split(",")))

    def test_seeded_defects_are_reported(self):
        def mutate_answers(d):
            p = d / ".copier-answers.yml"
            write(p, p.read_text(encoding="utf-8") + "favourite_colour: blue\n")

        defects = {
            "placeholder": (lambda d: write((d / "README.md"), "# <project-id>\n", encoding="utf-8"), "placeholder"),
            "jinja": (lambda d: write((d / "docs/notes.md"), "Value: {{ x }}\n", encoding="utf-8"), "placeholder"),
            "conflict": (lambda d: write((d / "README.md"), "<<<<<<< before\nx\n=======\ny\n>>>>>>> after\n", encoding="utf-8"), "conflict marker"),
            "rej": (lambda d: write((d / "AGENTS.md.rej"), "x\n", encoding="utf-8"), "leftover"),
            "missing": (lambda d: (d / "LICENSE").unlink(), "required file missing"),
            "link": (lambda d: write((d / "docs/notes.md"), "[x](missing.md)\n", encoding="utf-8"), "broken link"),
            "claude": (lambda d: write((d / "CLAUDE.md"), "@AGENTS.md\nExtra rule.\n", encoding="utf-8"), "CLAUDE.md"),
            "answers": (mutate_answers, "unknown keys"),
            "foreign-doc": (lambda d: (d / "docs/governance").mkdir(exist_ok=True) or
                            write((d / "docs/governance/agentic-operations.md"), "x\n", encoding="utf-8"),
                            "another profile"),
            "section-removed": (lambda d: write((d / "AGENTS.md"), 
                re.sub(r"(?s)## Prohibited.*?(?=\n## )", "", (d / "AGENTS.md").read_text(encoding="utf-8")),
                encoding="utf-8"), "missing cmn-prohibited"),
            "duplicate": (lambda d: write((d / "AGENTS.md"), 
                (d / "AGENTS.md").read_text(encoding="utf-8") + "\n- Prefer editing an existing file to creating a parallel one.\n",
                encoding="utf-8"), "repeats line"),
        }
        for name, (mutate, expected) in defects.items():
            with self.subTest(defect=name):
                dest = self.copy("ai-biz-example-assisted")
                (dest / "docs").mkdir(exist_ok=True)
                mutate(dest)
                code, out = self.validate(dest)
                self.assertEqual(code, 1, out)
                self.assertIn(expected, out)

    def test_private_without_data_ignore_fails(self):
        dest = self.copy("ai-home-example-assisted-private")
        gi = dest / ".gitignore"
        write(gi, gi.read_text(encoding="utf-8").replace("data/\n", ""))
        code, out = self.validate(dest)
        self.assertEqual(code, 1)
        self.assertIn("data/", out)

    def test_branch_and_title(self):
        dest = self.copy("ai-home-example-assisted-private")  # extra_types: perf
        self.assertEqual(self.validate(dest, "--meta-only", "--branch", "perf/faster", "--pr-title", "perf(db): add index")[0], 0)
        self.assertEqual(self.validate(dest, "--meta-only", "--branch", "feature/x")[0], 1)
        self.assertEqual(self.validate(dest, "--meta-only", "--pr-title", "Update things")[0], 1)
        self.assertEqual(self.validate(dest, "--meta-only", "--branch", "main")[0], 0)

    def test_compare_detects_template_drift(self):
        dest = self.copy("ai-biz-example-agentic")
        fresh = self.copy("ai-biz-example-agentic")
        self.assertEqual(self.validate(dest, "--compare-to", str(fresh))[0], 0)
        agents = dest / "AGENTS.md"
        write(agents, agents.read_text(encoding="utf-8").replace("first push of each branch", "first merge"),
                          encoding="utf-8")
        project_edit = agents.read_text(encoding="utf-8") + "- Use tabs.\n"
        write(agents, project_edit)
        code, out = self.validate(dest, "--compare-to", str(fresh))
        self.assertEqual(code, 1)
        self.assertIn("agt-autonomy", out)
        self.assertEqual(out.count("ERROR"), 1, out)  # the project-owned edit is not drift


    def test_recopy_reproduces_template_content(self):
        """The drift check's mechanism: copier recopy of the recorded version matches template-owned content."""
        dest = self.copy("ai-biz-example-multi-agent")
        self.init_repo(dest)
        agents = dest / "AGENTS.md"
        write(agents, agents.read_text(encoding="utf-8") + "- Project rule.\n")
        commit_all(dest, "docs: project rule")
        work = self.tmp / "recopy" / dest.name
        shutil.copytree(dest, work)
        run(COPIER + ["recopy", "--defaults", "--overwrite", "--quiet", str(work)])
        self.assertEqual(self.validate(dest, "--compare-to", str(work))[0], 0)


class TestLifecycle(TemplateTestCase):
    def new_template_version(self, tag, edit):
        edit(self.template)
        commit_all(self.template, "change for " + tag)
        git(self.template, "tag", tag)

    def test_update_preserves_project_content(self):
        dest = self.copy("ai-biz-example-agentic")
        self.init_repo(dest)
        agents = dest / "AGENTS.md"
        write(agents, agents.read_text(encoding="utf-8").replace(
            "<!-- Record language, formatting, test, and build conventions specific to this project here. -->",
            "- Python 3.12, formatted with the standard library only."))
        write((dest / "README.md"), "# Example\n\nProject-owned readme.\n")
        write((dest / "docs/decisions/0001-use-sqlite.md"), "# 0001. Use SQLite\n")
        (dest / "docs/agent").mkdir(parents=True)
        write((dest / "docs/agent/state.md"), "# Agent state\n\n- 2026-11-01: history entry\n")
        write((dest / "src.py"), "print('hello')\n")
        commit_all(dest, "feat: project content")
        before = {p: (dest / p).read_bytes() for p in
                  ("README.md", "docs/decisions/0001-use-sqlite.md", "docs/agent/state.md", "src.py")}
        project_before = self.sections(dest)["project"]

        def edit(tpl):
            p = tpl / "includes/governance/common/practices.md.jinja"
            write(p, p.read_text(encoding="utf-8") + "- Keep pull requests reviewable in one sitting.\n")
            r = tpl / "includes/governance/common/references.md.jinja"
            write(r, r.read_text(encoding="utf-8") + "- Template changelog: `docs/decisions/` in the template\n")
            readme = tpl / "template/README.md.jinja"
            write(readme, readme.read_text(encoding="utf-8") + "\nChanged seed.\n")
        self.new_template_version("v9.10.0", edit)

        self.update(dest, "--vcs-ref", "v9.10.0")
        self.assertEqual(list(dest.rglob("*.rej")), [])
        text = agents.read_text(encoding="utf-8")
        self.assertIn("Keep pull requests reviewable in one sitting.", text)
        self.assertIn("Template changelog", text)
        self.assertEqual(self.sections(dest)["project"], project_before)
        for rel, data in before.items():
            self.assertEqual((dest / rel).read_bytes(), data, rel)
        self.assertIn("_commit: v9.10.0", (dest / ".copier-answers.yml").read_text(encoding="utf-8"))
        self.assert_valid(dest)
        commit_all(dest, "chore(template): update to v9.10.0")
        self.assertGreaterEqual(int(git(dest, "rev-list", "--count", "HEAD").stdout.strip()), 3)

    def test_profile_round_trip(self):
        """assisted -> agentic -> multi-agent -> agentic -> assisted keeps project records."""
        dest = self.copy("ai-biz-example-assisted")
        self.init_repo(dest)
        write((dest / "docs/decisions/0001-record.md"), "# 0001. Record\n")
        commit_all(dest, "docs: add decision")
        expected_files = {
            "assisted": (set(), {"docs/governance/agentic-operations.md", "docs/governance/multi-agent-operations.md"}),
            "agentic": ({"docs/governance/agentic-operations.md"}, {"docs/governance/multi-agent-operations.md"}),
            "multi-agent": ({"docs/governance/agentic-operations.md", "docs/governance/multi-agent-operations.md"}, set()),
        }
        for step, profile in enumerate(["agentic", "multi-agent", "agentic", "assisted"]):
            with self.subTest(step=step, profile=profile):
                project_before = self.sections(dest)["project"]
                self.update(dest, "--vcs-ref=:current:", "--data", "profile=" + profile)
                present, absent = expected_files[profile]
                for rel in present:
                    self.assertTrue((dest / rel).is_file(), rel)
                for rel in absent:
                    self.assertFalse((dest / rel).exists(), rel)
                self.assertEqual(self.sections(dest)["project"], project_before)
                self.assertEqual(list(dest.rglob("*.rej")), [])
                self.assertIn("profile: " + profile, (dest / ".copier-answers.yml").read_text(encoding="utf-8"))
                self.assertIn(TAG, (dest / ".copier-answers.yml").read_text(encoding="utf-8"))
                if profile == "agentic" and step == 0:
                    (dest / "docs/agent").mkdir(parents=True)
                    write((dest / "docs/agent/state.md"), "# Agent state\n\n- 2026-11-27: first delegation\n",
                                                              encoding="utf-8")
                self.assert_valid(dest)
                commit_all(dest, "chore(profile): switch to " + profile)
        self.assertIn("first delegation", (dest / "docs/agent/state.md").read_text(encoding="utf-8"))
        self.assertTrue((dest / "docs/decisions/0001-record.md").is_file())
        self.assertEqual(self.sections(dest).keys() - {"project"},
                         self.sections(self.copy("ai-biz-example-assisted")).keys() - {"project"})

    def test_rollback_restores_tree(self):
        dest = self.copy("ai-biz-example-assisted")
        self.init_repo(dest)
        before = tree_digest(dest)
        self.update(dest, "--vcs-ref=:current:", "--data", "profile=multi-agent")
        self.assertNotEqual(tree_digest(dest), before)
        git(dest, "reset", "-q", "--hard")
        git(dest, "clean", "-q", "-d", "-f")
        self.assertEqual(tree_digest(dest), before)


class TestRepositoryDocs(unittest.TestCase):
    def test_relative_links_resolve(self):
        for path in list(ROOT.glob("*.md")) + list((ROOT / "docs").rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            text = re.sub(r"(?s)```.*?```", "", text)
            for target in re.findall(r"\]\(([^)\s]+)\)", re.sub(r"`[^`]*`", "", text)):
                if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                local = target.split("#")[0]
                with self.subTest(file=path.name, target=target):
                    self.assertTrue((path.parent / local).exists())


if __name__ == "__main__":
    unittest.main()
