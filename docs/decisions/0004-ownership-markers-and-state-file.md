# 0004. Ownership classes, AGENTS.md markers, and the state file

- Date: 2026-11-27
- Status: accepted (owner decisions D10, D11), with one change from the design (below)

## Decision

1. Three ownership classes, mapped to Copier mechanisms (table in `procedure-update-and-profile-change.md`, Section 2): template-controlled (rendered, replaced on update), jointly managed (rendered, three-way merged), project-controlled (never generated, or created once via `_skip_if_exists`).
2. `AGENTS.md` keeps every always-needed rule inline, because tools do not share an import syntax. Each section heading carries a marker: `<!-- template-owned id=<layer>-<name> -->`, and the final `## Project` heading carries `<!-- project-owned ... -->`. A marker ends at the next marker; the project section runs to the end of the file. Markers sit on the heading line, so they add no lines. One marker per section, not per rule: the validator checks section order and layers, and rejects repeated rule lines.
3. The project section is seeded from the `purpose` and `scope` answers once and is project-owned afterwards. Template changes never touch it, so updates merge cleanly; the tests confirm this with a template change directly above it.
4. Agentic state lives at `docs/agent/state.md`, project-owned. Decisions live in `docs/decisions/`, project-owned.

## Change from the approved design

The design seeded `docs/agent/state.md` through `_skip_if_exists`. A test showed that Copier deletes a profile-conditional file on downgrade even after the project edited it, which would remove the history the state file exists to keep. The template therefore never creates the state file. `docs/governance/agentic-operations.md` holds its skeleton, the agent creates it before the first delegation, and the validator warns while it is missing. Because the template never rendered it, no update or profile change can delete it.

## Consequences

- Downgrading to assisted keeps `docs/agent/state.md` as a historical record; the assisted `AGENTS.md` does not reference it.
- `.copier-answers.yml` is the only version record (no extra governance-version file).
