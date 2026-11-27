# 0003. Link-don't-copy amended for offline resilience

- Date: 2026-11-27
- Status: accepted (owner decision D3)

## Context

The standard said standards are linked from this template and never copied. Generated repositories also need governance that works when the template is unavailable, including hosted sessions without `<projects-root>`. Links pointed at `blob/main`, so their meaning changed silently whenever a standard changed.

## Decision

| Resource | Handling |
|---|---|
| Human-readable standards (`docs/standard-*.md`) | Stay here only. Generated repositories link to them pinned to the release they were generated from (`blob/vX.Y.Z/...`, or a commit permalink for an untagged render). Updating the template moves the pin |
| Governance needed to operate (`AGENTS.md`, `docs/governance/*`) | Rendered into each repository, template-owned, changed only through `copier update` |
| Machine-checkable rules (naming, domains, required files, section layout) | Rendered into `scripts/check_governance.py` |
| Efficiency routing | Unchanged: an optional sibling clone, not a copy |

Amended rule (in `standard-naming-project.md`, Section 9): human-readable standards are linked, never copied. Files rendered by the template and tracked by `.copier-answers.yml` are not copies; they are template-owned and change only through the template.

Rejected: Git submodules (network and authentication at clone time; friction in hosted sessions; duplicate version tracking), Git subtree (a physical copy without answer-aware merging), unpinned links (silent meaning changes).

## Consequences

- Generated repositories work offline; only updates and the CI drift check need the template.
- Reading a standard needs network access, but no operation depends on it.
