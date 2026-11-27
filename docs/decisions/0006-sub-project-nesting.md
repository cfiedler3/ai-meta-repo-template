# 0006. Sub-project nesting

- Date: 2026-11-27
- Status: proposed

## Context

`standard-naming-project.md` Section 7 deferred sub-project nesting rules (for example, `home-maint` and `home-maint-porch`). Without them, a child project's name cannot be validated against its parent, a child segment cannot be told apart from a descriptor, and renames that cascade from a parent are undefined. Existing projects waiting on this rule are a household maintenance parent and its gardening child.

## Decision

1. **Separate project or folder.** A sub-project is a separate project only when it has its own lifecycle, context, and assistant project. Otherwise it is a folder inside the parent (for example, an individual build is `docs/projects/<name>.md` in the parent, not a project).
2. **Name.** A child's Project ID is the parent's Project ID, without its visibility suffix, plus exactly one `child` segment: `ai-home-maint` → `ai-home-maint-porch`.
3. **Child versus descriptor.** Descriptors are the closed list in Section 7 (`-api`, `-ui`, `-scripts`, `-infra`). Any other segment after a parent's ID is a child. Segment order: `[backing]-[domain]-[project]-[child]-[descriptor]-[visibility]`.
4. **Same backing and domain.** A child carries the parent's backing prefix and domain, as components already do. A mixed pair (`hm-` parent, `ai-` child) is not allowed; promoting or demoting one promotes or demotes both.
5. **Depth and layout.** One level of nesting only. Local folders stay flat at `<projects-root>/<Project ID>/` (Section 2); a child is never cloned or stored inside its parent's folder.
6. **Parent first.** The parent project exists before any child is created.
7. **Cascading rename.** Renaming a parent renames every child, on all three artifacts.
8. **Visibility.** A child may add `-private` independently of its parent; it remains the final segment.

## Consequences

- The Copier validator and `scripts/check_governance.py` are unchanged. Neither can see other projects, so parent existence and same-backing remain documented rules checked by the Section 10 checklist. A test case confirms child-style IDs pass both validators.
- One level of depth keeps cascading renames small.
- Rejected: dotted or nested folder layouts (break the flat `<projects-root>` rule and tooling that assumes it); unlimited depth (rename cascades grow, IDs grow past readable length); letting a child differ in backing (breaks the single-identity model and the tooling matrix).
