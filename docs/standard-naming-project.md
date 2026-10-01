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
[backing]-[domain]-[project]-[descriptor]
```

| Segment | Required | Meaning |
|---|---|---|
| `backing` | Yes | Where the source of truth lives (Section 4) |
| `domain` | Recommended | Area of life or work (Section 5) |
| `project` | Yes | The initiative name (Section 6) |
| `descriptor` | No | Component or scope qualifier (Section 7) |

**Core rules**

- Lowercase only
- Hyphens (`-`) separate words; no spaces, underscores, or special characters
- Concise, descriptive, readable at a glance
- No version numbers (use tags, releases, or branches)

**Examples**

- `ai-biz-example-shop`
- `ai-am-printer-model-slicer-profiles`
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
2. `hm-` is for projects whose content does not warrant version control. If a project's loss would matter, it is `ai-`.
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

Component projects carry the same backing and domain prefixes as their parent.

Sub-project nesting rules (for example, `home-maint` and `home-maint-porch`) are deferred.

---

## 8. Retirement

| Project type | Retirement action |
|---|---|
| `ai-` | Archive the repository on the hosting platform; remove it from the connector; delete the local clone |
| `hm-` | Move the folder to `<projects-root>/Archive/` |

Archived projects and backup archives (`.zip`) are exempt from this standard.

---

## 9. Where Standards Live

- Project and platform standards live in `ai-meta-repo-template/docs/` only.
- Other projects link to them; they never copy them. The template is public, so public repositories may link to it as well.
- Project-specific conventions live in that project's README or `AGENTS.md`.

---

## 10. Validation Checklist

- [ ] Exactly one backing prefix (`ai-` or `hm-`) in first position
- [ ] `ai-` only if a repository exists and is in the connector; `hm-` only if no repository exists
- [ ] Domain from the Section 5 table, or omitted
- [ ] Lowercase, hyphen-separated, no version numbers
- [ ] Assistant project, repository, and local folder all carry the ID exactly
- [ ] Platform-specific checks completed (see the platform standard)

---

## 11. Anti-Patterns

- `biz-example-shop` (missing backing prefix)
- `ai-hm-example` (two backing prefixes)
- Repository `ai-personal-example` with assistant project `ai-example` (misaligned)
- `ai-example` folder with no repository (wrong backing prefix)
- A copy of this document in another repository

---

## 12. Change Log

| Date | Change |
|---|---|
| 2026-10-01 | Added `meta-` domain; template is `ai-meta-repo-template` (public) and no longer exempt |
| 2026-10-01 | Initial version. Extracted vendor-neutral content from `github-naming-standard.md` (now `standard-naming-github.md`); introduced Project ID, backing prefix (`ai-`/`hm-`), `home-` and `trip-` domains, tooling matrix, retirement rules |
