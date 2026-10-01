# GitHub Naming Standard

## 1. Purpose

Define the GitHub-specific rules for repositories. Project identity, naming format, backing and domain prefixes, and cross-artifact alignment are defined in [`standard-naming-project.md`](standard-naming-project.md); this document adds only what is specific to GitHub as a hosting platform.

---

## 2. Repository Name

A repository's name is the Project ID, exactly as defined in the project standard. Every repository is an `ai-` project; there are no `hm-` repositories.

**Examples:**
- `ai-biz-example-shop`
- `ai-am-printer-model-slicer-profiles`
- `ai-example-private`

---

## 3. Repository Creation

- Create from `ai-meta-repo-template` so the repository carries `AGENTS.md`, the assistant instruction file that imports it, and the standard license.
- Create with private visibility unless public visibility has been explicitly approved. `meta-` repositories are public by default, since public repositories must be able to link to them.
- Add the repository to the assistant's GitHub connector at creation.
- Add a `protect-main` branch ruleset: require a pull request, block force pushes, squash merge only.
- Clone to `<projects-root>/<Project ID>/`.

---

## 4. Intended Private Visibility (Optional)

Use the suffix `-private` for a repository intended to remain private. Place it last, after any descriptor: `ai-example-api-private`. Keep backing and domain prefixes unchanged; do not use `private-ai-` or `ai-private-`.

| Name | Meaning |
|---|---|
| `ai-example` | Project repository; visibility must be checked |
| `ai-example-private` | Related repository intended to remain private |
| `ai-example-api-private` | API component intended to remain private |

The suffix communicates intent only. GitHub's visibility setting controls access; verify it directly rather than inferring it from the name.
See [GitHub repository visibility](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories).

- An unmarked repository is neither automatically public nor approved for publication.
- Publishing a repository or changing it to public requires separate explicit approval and review of the files and Git history intended for publication. Removing `-private` does not grant approval or change access settings.
- Keep private lesson records and supporting evidence outside tracked repository content, even when the repository is private.
- Maintain explicit project inclusion and exclusion lists for discovery. `ai-*` finds all project repositories and `ai-*-private` finds names marked private; neither filter establishes actual visibility or permission to inspect content.
- Existing repositories need not be renamed solely to adopt this marker. Any separately authorized rename must preserve alignment with the assistant project and local folder.

---

## 5. Assistant GitHub Connector

- The connector is installed with access to selected repositories only.
- The selected list must equal the set of active `ai-` repositories. A missing active repository, or a present archived repository, is drift and is corrected.
- New repositories are added to the connector manually at creation; archived repositories are removed at archive time.

---

## 6. Retirement

| Action | When |
|---|---|
| Archive | The repository represents real past work or may be referenced again. Archived repositories remain read-only on GitHub, are removed from the connector, have their local clone deleted, and are exempt from naming rules |
| Delete | Throwaway or test repositories with no history worth keeping |

Archive is the default; delete only when certain.

---

## 7. Repository Structure Pattern

**Pattern: Multi-repo**

Each component, service, or workstream gets its own repository.

### Decision

Multi-repo was chosen over monorepo because:
- Simpler CI/CD — each repo owns its own pipeline
- Cleaner access control — permissions scoped per repo
- Reduced complexity — no monorepo tooling (Nx, Turborepo, etc.)
- Aligns with the descriptor convention — `-api`, `-ui`, `-infra` map directly to individual repos

### Rules

- One repository per component or service
- Use descriptors (project standard, Section 7) to name each repo consistently
- Do not combine unrelated components into a single repository
- Component repositories carry the same backing and domain prefixes as their parent

### When to Create a New Repo

- Has its own deployment pipeline or release cycle
- Could be developed or maintained independently
- Maps to a distinct descriptor (`-api`, `-ui`, `-infra`, `-scripts`)

### When NOT to Create a New Repo

- A single script or utility that belongs inside an existing repo
- A minor variation of an existing component (use branches or folders)
- Temporary or experimental work (use a branch)

### Example

| Component | Repository |
|---|---|
| Core project | `ai-biz-example-shop` |
| Backend API | `ai-biz-example-shop-api` |
| Frontend UI | `ai-biz-example-shop-ui` |
| Infrastructure | `ai-biz-example-shop-infra` |

---

## 8. Validation Checklist

Before creating a repo, confirm:

- [ ] Name passes the project standard checklist
- [ ] Created from `ai-meta-repo-template`
- [ ] Private by default; any public creation explicitly approved after content and history review
- [ ] Added to the assistant's GitHub connector
- [ ] `protect-main` ruleset applied
- [ ] Cloned to `<projects-root>` under the same name
- [ ] If used, `-private` is the final suffix
- [ ] Discovery inclusion and exclusion recorded separately when planning a review

---

## 9. Future Extensions

- Branch naming conventions
- Commit message standards

---

## 10. Change Log

| Date | Change |
|---|---|
| 2026-10-01 | Template is `ai-meta-repo-template`; `meta-` repositories public by default; `protect-main` ruleset required |
| 2026-10-01 | Renamed from `github-naming-standard.md`. Trimmed to GitHub-specific content; identity, prefixes, and alignment moved to `standard-naming-project.md`. Added connector and retirement sections |
| 2026-09-30 | Added governance prefix (`ai-` / `hm-`), rules and exemptions, `am-` domain, assistant project alignment |
