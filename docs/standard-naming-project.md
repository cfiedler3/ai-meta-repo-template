# Project Naming Standard

## 1. Purpose

Define a single identity for every project so that it can be located and managed consistently across all the places it exists: AI assistant projects, source repositories, and the local filesystem.

This standard is vendor-neutral. Platform-specific rules (repository visibility, archiving, connector configuration) live in platform standards that reference this one, such as `standard-naming-github.md`.

---

## 2. The Project Is the Unit

A project is any ongoing area of work with its own context, files, and decisions. It exists the moment an assistant project or a local folder is created for it. A source repository is optional.

Every project has exactly one **Project ID**. Every artifact of the project carries that ID exactly:

| Artifact | Name |
|---|---|
| Assistant project | Project ID |
| Source repository (if any) | Project ID |
| Local folder | `<projects-root>/<Project ID>/` |

`<projects-root>` is the single top-level folder for all projects on a machine. It is defined once per machine and is not part of any Project ID.

Renaming a project means renaming all three. Adding or removing a repository changes the backing prefix (Section 4) and is therefore a rename.

---

## 3. Project ID Format

```
[backing]-[domain]-[project]-[child]-[descriptor]-[visibility]
```

| Segment | Required | Meaning |
|---|---|---|
| `backing` | Yes | Where the source of truth lives (Section 4) |
| `domain` | Recommended | Area of life or work (Section 5) |
| `project` | Yes | The initiative name (Section 6) |
| `child` | No | Sub-project of an existing parent project (Section 7) |
| `descriptor` | No | Component or scope qualifier (Section 7) |
| `visibility` | No | `private` only: the project is intended to remain private. Always the final segment. Platform rules define what it means for a repository (see `standard-naming-github.md`, Section 4) |

**Core rules**

- Lowercase only
- Hyphens (`-`) separate words; no spaces, underscores, or special characters
- Concise, descriptive, readable at a glance
- No version numbers (use tags, releases, or branches)
- A visibility suffix is part of the Project ID and appears on every artifact, not only the repository
- A visibility suffix carries required actions, not only a name. For a repository they are listed in `standard-naming-github.md`, Section 4

**Examples**

- `ai-biz-example-shop`
- `ai-am-printer-model-slicer-profiles`
- `ai-home-example-private`
- `hm-home-finance`
- `hm-trip-example-2026`

---

## 4. Backing Prefix (Required)

The first segment states where the project's source of truth lives. It is observable, not a judgment call.

| Prefix | Backing store | Tooling |
|---|---|---|
| `ai-` | Source repository on the hosting platform, cloned to the local folder | Assistant chat (via repository connector) and assistant coding agent; the agent may commit under the repository's governance rules |
| `hm-` | Local filesystem only; no repository | Assistant chat only (via filesystem access); no version control, no agent commits, no coding agent |

**Rules**

1. A repository is always `ai-`. Every repository is created from `ai-meta-repo-template` and carries `AGENTS.md` (imported by the assistant's instruction file).
2. `hm-` is for projects whose content does not warrant version control. Version control and backup are separate needs: a project is `ai-` when it needs version history or agent commits, and any project whose loss would matter needs a backup, whatever its prefix. Content kept out of the repository on purpose, such as a `-private` project's `data/` folder (`standard-naming-github.md`, Section 4), is not protected by version control.
3. Promotion (`hm-` → `ai-`): initialize the repository, push, register it with the assistant's repository connector, rename all artifacts. Demotion is the reverse.
4. The assistant's repository connector grants access to all active `ai-` repositories and nothing else. Any mismatch is drift and is corrected.

### Tooling matrix

| Project type | Assistant chat | Coding agent |
|---|---|---|
| `ai-` | Yes | Yes |
| `hm-` | Yes (filesystem access) | No |

---

## 5. Domain Prefix (Recommended)

The domain names the area of life or work. Use one domain, or none if it adds no clarity.

| Prefix | Usage | Example |
|---|---|---|
| `am-` | Additive manufacturing (3D printing) | `ai-am-printer-model-slicer-profiles` |
| `biz-` | Business initiatives | `ai-biz-example-shop` |
| `home-` | Household matters, shared or co-managed (finance, maintenance, property) | `hm-home-finance` |
| `meta-` | Projects that scaffold, govern, or support other projects (templates, standards, shared workflows, shared agent assets) | `ai-meta-repo-template` |
| `personal-` | Individual projects owned solely by the author (career, site, certifications) | `ai-personal-example-site` |
| `trip-` | Travel planning | `hm-trip-example-2026` |

**Rules**

- Domains represent distinct areas, not volume. A domain with one project is valid; a sub-category of an existing area is not a new domain.
- `home-` wins over `personal-` when scope is ambiguous; it is easier to widen a shared scope than to narrow one.
- Adding a domain requires updating this table.

---

## 6. Project Segment

- Maps directly to the initiative name
- May contain standardized words such as `cert`, `finance`, `maint`
- Abbreviations only if standardized and recognizable (`api`, `ui`, `am`, `hm`, `cert`); project-specific codes (hardware models, tool names) must be documented in the project's README

---

## 7. Descriptor (Optional)

Add a suffix when a project has separately managed components.

| Suffix | Purpose |
|---|---|
| `-api` | Backend / API service |
| `-ui` | Frontend / UI |
| `-scripts` | Automation / scripts |
| `-infra` | Infrastructure / configuration |

Component projects carry the same backing and domain prefixes as their parent. A visibility suffix, if used, follows the descriptor (`ai-example-api-private`).

### Sub-projects

A sub-project is a separate project with its own lifecycle, context, and assistant project, nested under a parent. Work that lacks these is a folder inside the parent, not a sub-project. See ADR 0006.

1. A child's Project ID is the parent's Project ID (without its visibility suffix) plus exactly one `child` segment: `ai-home-maint` → `ai-home-maint-porch`.
2. Descriptors are the closed list in the table above. Any other segment after a parent's ID is a child. Order: `[project]-[child]-[descriptor]-[visibility]`.
3. A child carries the parent's backing prefix and domain. Promoting or demoting one promotes or demotes both.
4. One level of nesting only. Local folders stay flat (Section 2); a child is never stored inside its parent's folder.
5. The parent exists before any child is created.
6. Renaming a parent renames every child, on all three artifacts.
7. A child may add `-private` independently of its parent.

---

## 8. Retirement

| Project type | Retirement action |
|---|---|
| `ai-` | Preserve local-only content (below); archive the repository on the hosting platform; remove it from the connector; delete the local clone |
| `hm-` | Move the folder to `<projects-root>/Archive/` |

**Preserve local-only content before deleting a clone.** A clone can hold content the repository does not, including a `-private` project's untracked `data/` folder.

1. List local-only content: `git status --short --ignored` (untracked and ignored files), `git log --branches --not --remotes --oneline` (unpushed commits), and `git stash list`.
2. Push or deliberately discard each unpushed commit and stash.
3. Copy every untracked or ignored file still needed to `<projects-root>/Archive/<Project ID>-local.zip`, then open the archive and confirm it lists those files.
4. Delete the clone only after step 3 is confirmed.

Archived projects and backup archives (`.zip`) are exempt from this standard.

---

## 9. Where Standards Live

- Project and platform standards live in `ai-meta-repo-template/docs/` only.
- Other projects link to them; they never copy them. The template is public, so public repositories may link to it as well.
- Generated repositories link to the standards pinned to the template release they were generated from; `copier update` moves the pin.
- Files rendered by the template and tracked by the repository's `.copier-answers.yml` (for example `AGENTS.md` and its governance procedures) are not copies. They are template-owned and change only through the template (ADR 0003).
- Project-specific conventions live in that project's README or `AGENTS.md`.

---

## 10. Validation Checklist

- [ ] Exactly one backing prefix (`ai-` or `hm-`) in first position
- [ ] `ai-` only if a repository exists and is in the connector; `hm-` only if no repository exists
- [ ] Domain from the Section 5 table, or omitted
- [ ] Lowercase, hyphen-separated, no version numbers
- [ ] Visibility suffix, if used, is `-private`, is last, and appears on every artifact
- [ ] Assistant project, repository, and local folder all carry the ID exactly
- [ ] Sub-project: parent exists, same backing prefix and domain, one level deep (Section 7)
- [ ] Platform-specific checks completed (see the platform standard)

---

## 11. Anti-Patterns

- `biz-example-shop` (missing backing prefix)
- `ai-hm-example` (two backing prefixes)
- Repository `ai-personal-example` with assistant project `ai-example` (misaligned)
- Repository `ai-example-private` with assistant project `ai-example` (visibility suffix dropped from one artifact)
- `ai-private-example` or `ai-example-private-api` (visibility suffix not last)
- `ai-example` folder with no repository (wrong backing prefix)
- `ai-home-maint-porch-front` (two levels of nesting)
- `hm-home-maint` with child `ai-home-maint-porch` (child backing differs from parent)
- A child folder inside its parent's folder
- A copy of this document in another repository

---

## 12. Change Log

| Date | Change |
|---|---|
| 2026-11-27 | Section 3: optional `child` segment. Section 7: sub-project nesting rules replace the deferral (ADR 0006). Sections 10, 11: checks and anti-patterns |
| 2026-11-27 | Section 4: version control and backup are separate needs. Section 8: preserve local-only content before deleting a clone |
| 2026-11-27 | Section 9: pinned links; template-rendered files are not copies (ADR 0003) |
| 2026-11-14 | Section 3: a visibility suffix carries required actions, defined in the platform standard |
| 2026-11-07 | Added optional `visibility` segment (`-private`) to the Project ID format; it is part of the ID on every artifact. Updated checklist and anti-patterns |
| 2026-10-01 | Added `meta-` domain; template is `ai-meta-repo-template` (public) and no longer exempt |
| 2026-10-01 | Initial version. Extracted vendor-neutral content from `github-naming-standard.md` (now `standard-naming-github.md`); introduced Project ID, backing prefix (`ai-`/`hm-`), `home-` and `trip-` domains, tooling matrix, retirement rules |
