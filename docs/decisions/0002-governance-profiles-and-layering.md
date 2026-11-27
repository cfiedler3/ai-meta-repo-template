# 0002. Governance profiles, layering, and classification of existing rules

- Date: 2026-11-27
- Status: accepted (owner decisions D4, D5, D6, D7, D8, D12, D17, D18)

## Context

The previous `AGENTS.md` assumed one way of working: per-action approval for every change. Agentic and multi-agent development need delegated authority, approval gates, and coordination rules, and these contradict per-action approval if both appear in one file.

## Decision

1. Three profiles: `assisted`, `agentic`, `multi-agent` (definitions in `standard-governance-profiles.md`). Common rules apply to all; assisted and agentic each add one autonomy section; multi-agent reuses agentic unchanged and adds its own sections. Inheritance is defined only in `includes/governance/manifest.jinja`.
2. Agentic approval gates: first push of each branch, opening a pull request, out-of-scope actions, irreversible actions, and security or privacy uncertainty. Merging stays prohibited everywhere.
3. Domain list: the committed standard (`am`, `biz`, `home`, `meta`, `personal`, `trip`). `ui` remains a descriptor (`-ui`), and `automation` is not a domain. Adding either is a change to `standard-naming-project.md`, Section 5, plus `copier.yml`, and a test fails until both agree.
4. `efficiency_routing` defaults to off in generated repositories, because it fails in sessions without the sibling clone. This repository keeps it enabled.

## Classification of the previous rules

Section numbers refer to the previous `AGENTS.md` (commit `1fb307a`). Nothing was dropped without a destination below.

| Previous rule | Class | New location | Change in meaning |
|---|---|---|---|
| §1 Project paragraph | Project | `## Project` (seeded from `purpose`, `scope`) | None |
| §1 Project ID, backing, visibility lines | Common | `cmn-header`, rendered from answers; validator checks them | None |
| §2 Repository is the source of truth; settings hold a pointer | Common | `cmn-authority` 3 | None |
| §2 Standards linked, never copied | Supporting standard | `standard-naming-project.md` §9, amended (ADR 0003) | Generated governance is not a copy |
| §3 "AI systems are collaborators, not autonomous agents"; approval at each step; ask when in doubt | **Assisted** | `ast-autonomy` | No longer universal; agentic replaces it with delegated authority |
| §3 Behavioral foundation 1 (don't assume, surface trade-offs) | Common | `cmn-practices` 1 | Reworded as instructions |
| §3 Behavioral foundation 2–3 (minimum change; touch only what you must) | Common | `cmn-practices` 3 | Reworded |
| §3 Behavioral foundation 4 (success criteria; verify) | Common | `cmn-practices` 2; agentic `agt-completion` | Agentic adds explicit completion criteria |
| §4 Permitted without confirmation | **Assisted** | `ast-autonomy` | Agentic permits more inside a delegation |
| §4 Requires confirmation, per action and per session | **Assisted** | `ast-autonomy` | Agentic uses gates instead; without a delegation, agentic also requires per-action approval |
| §4 Prohibited: commit to `main` | Common | `cmn-prohibited` | None |
| §4 Prohibited: merging pull requests | Common | `cmn-prohibited` | None |
| §4 Prohibited: deleting branches, files, or history | Common | `cmn-prohibited` | **Narrowed (D7):** no history rewrite; delete only branches or tags you created; delete files only within the approved change |
| §4 Prohibited: credentials and secrets | Common | `cmn-prohibited` | Adds personal data explicitly |
| §4 Prohibited: `-private` content | Common (conditional) | `cmn-data-handling` | None; rendered only for `-private` |
| §4 Prohibited: settings changes; irreversible actions | Common | `cmn-prohibited` | None |
| §5 Rules 1–6 (branch, Conventional Commits, one change per PR, squash, no history rewrite, atomic commits) | Common | `cmn-source-control`, `cmn-prohibited` | PR title must also be a Conventional Commit (enforced in CI) |
| §5 "[project] may add project-specific types" | Common (answer) | `extra_types` question | Enforced by the validator instead of free text |
| §6 PR template use; API caveat; real line breaks | Common | `cmn-source-control` 4 | None |
| §6 Governance checklist always completed | Common | PR template, profile-aware (D8) | The owner-request line is assisted-only; agentic confirms the delegation and gate approval; multi-agent adds independent verification |
| §7 Read this file and the README first | Redundant | Removed | Tools load `AGENTS.md` automatically; agentic session start is in `agentic-operations.md` |
| §7 No new tools unless value exceeds cost | Common | `cmn-practices` | None |
| §7 Prefer editing; small changes | Common | `cmn-practices` | None |
| §7 Ask one question rather than guessing | Common | `cmn-practices` 1 | Agentic escalation adds when to stop |
| §7 Docs current in the same PR | Common | `cmn-practices` | None |
| §7 No binary or media in context | Common | `cmn-practices` | None |
| §7 Worker agents never inherit the session model | **Multi-agent** (D5) | `mag-models-cost` | Stated as a principle: name the model, least costly that is reliable |
| §8 Optional modules / efficiency routing | Optional capability | `cmn-modules`, rendered when `efficiency_routing` is true | Default off (D17); toggled by answer, not by editing the table |
| §9 Repository layout tree | Obsolete | Removed | Inferable from the repository; overviews do not help agents |
| §10 Conventions [project] | Project | `## Project` / `### Conventions` | None |
| §11 Related standards | Common | `cmn-references`, links pinned to the release | Links no longer follow `main` |
| §12 Data handling [project] | Common (conditional) + answers | `cmn-data-handling`; `sensitive_data`, `tracked_content` questions | Fields come from answers; rendered only for `-private` |
| README post-instantiation steps 1–4, 8 | Procedure | Automated by Copier answers and conditional rendering | No manual edits |
| README steps 5–7 (connector, ruleset, project settings) | Procedure | `procedure-provisioning.md` §6 | Adds the required `governance` check |
| README "apply changes forward" | Obsolete | Replaced by `copier update` | — |
| `standard-naming-github.md` §9 future extensions | Obsolete | Removed; branch and commit rules live in `AGENTS.md` | — |
| `standard-project-instructions.md` cold-session rules | Supporting standard | Same file, profile-aware | Agentic bootstrap rules added |

New rules with no previous equivalent: instruction precedence and treating fetched content as data (`cmn-authority`); all agentic and multi-agent sections.

## Consequences

- A generated `AGENTS.md` is 71–138 lines depending on profile and options.
- Changing a common rule now changes every profile; the tests show where.
