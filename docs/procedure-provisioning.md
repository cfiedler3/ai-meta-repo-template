# Procedure: Provisioning a Repository

Create a new `ai-` repository from this template with Copier. Rules for names and visibility are in `standard-naming-project.md` and `standard-naming-github.md`; this procedure covers the steps.

## 1. Prerequisites

| Need | Check | Notes |
|---|---|---|
| Python 3.9+ | `python --version` | Windows, Linux, macOS |
| Git | `git --version` | |
| Copier 9.13+ (tested 9.19.1) | `copier --version` | Install once: `uv tool install copier==9.19.1` or `pipx install copier==9.19.1`. Without installing: prefix commands with `uvx --from copier==9.19.1` |
| GitHub CLI (publication only) | `gh auth status` | Optional; repository creation can also be done in the GitHub web UI |

Template source, in order of preference:

- `gh:cfiedler3/ai-meta-repo-template` (remote; required for the CI drift check)
- a local clone at `<projects-root>/ai-meta-repo-template` (works offline; the drift check is skipped)

Always pin a release: `--vcs-ref vX.Y.Z`. Without it Copier uses the latest tag.

## 2. Interactive (owner)

```
cd <projects-root>
copier copy --vcs-ref vX.Y.Z gh:cfiedler3/ai-meta-repo-template <project-id>
```

Copier asks for the Project ID, purpose, scope, profile, visibility, owner, license details, efficiency routing, extra commit types, and, for `-private` IDs, what is sensitive and what may be tracked. Invalid Project IDs are rejected with the reason.

## 3. Non-interactive (assistant or script)

Write an answers file (see `tests/fixtures/` for complete examples):

```yaml
project_id: ai-biz-example-shop
purpose: One sentence.
scope: One sentence.
profile: assisted
visibility: private
owner: <github-account>
copyright_holder: <name>
copyright_year: 2026
efficiency_routing: false
```

Then:

```
copier copy --defaults --data-file answers.yml --vcs-ref vX.Y.Z gh:cfiedler3/ai-meta-repo-template <project-id>
```

`--defaults` makes Copier fail instead of prompting when an answer is missing. Delete the answers file afterwards; `.copier-answers.yml` in the new repository is the record.

## 4. Initialize and validate

```
cd <project-id>
git init -b main
git add -A
git commit -m "chore: initialize from ai-meta-repo-template"
python scripts/check_governance.py
```

The check must report 0 errors. A warning that the local folder name differs from the Project ID means the folder is misnamed.

## 5. Publish (explicit owner approval only)

An assistant runs this only after the owner approves it in the current session. Public visibility also needs the review in `standard-naming-github.md`, Section 4.

```
gh repo create <project-id> --private --source . --push
```

## 6. Manual steps

1. Add the repository to every assistant GitHub integration in use (chat connector and coding-agent app have separate lists).
2. Add the `protect-main` ruleset: require a pull request, block force pushes, squash merge only, and require the `governance` status check. On GitHub Free, rulesets are enforced on public repositories only; on private repositories the check still runs but does not block merging.
3. Create the assistant project instructions from `standard-project-instructions.md`.
4. For a `-private` ID, complete the required actions in `standard-naming-github.md`, Section 4, before committing project content.
5. Agentic and multi-agent profiles: create `docs/agent/state.md` from the skeleton in `docs/governance/agentic-operations.md` when the owner grants the first delegation.

## 7. Hosted sessions

Hosted coding sessions (for example, web or mobile coding agents) usually can install Copier from the package registry and reach GitHub, but cannot see `<projects-root>` or Windows paths, and may not be allowed to create repositories.

1. The owner creates an empty repository named with the Project ID and grants the session access.
2. The session clones it, runs Section 3 into the clone with `--overwrite`, then Section 4 without `git init`, and pushes a branch after approval.
3. The owner merges the initial pull request.

Sessions that cannot run commands (chat with a repository connector only) cannot provision; they read the generated `AGENTS.md`.

## 8. Change Log

| Date | Change |
|---|---|
| 2026-11-27 | Initial version: Copier-based provisioning replaces the GitHub template-repository flow (ADR 0001) |
