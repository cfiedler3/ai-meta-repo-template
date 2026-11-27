# 0005. Deterministic enforcement scope

- Date: 2026-11-27
- Status: accepted (owner decisions D13, D18)

## Context

`AGENTS.md` is guidance, not enforcement. Studies of agent context files find instructions are generally followed, but file length and structure have little measurable effect on adherence, and adherence decays within long sessions. Critical rules therefore need checks that do not depend on the agent.

## Decision

| Requirement | Mechanism |
|---|---|
| Project ID, domains, `-private` rules | Copier validator at input; `scripts/check_governance.py` re-checks (a test keeps both in agreement) |
| Branch name, Conventional Commit PR title | Validator in CI (`--branch`, `--pr-title`). The PR title is checked instead of every commit, because squash merge makes it the commit on `main` |
| Branch protection, PR required, squash only, no force push | Existing `protect-main` ruleset |
| Required files per profile; files from another profile | Validator |
| Section layout per profile, layer exclusivity, repeated rules | Validator; tests for inheritance and snapshots |
| Template-controlled content unchanged | CI drift job: `copier recopy` of the recorded version, compared by the validator; skipped with a warning when the template is unreachable |
| Project content preserved on update | Tests in this repository's CI |
| Unresolved placeholders, conflict markers, `.rej` files, broken relative links | Validator; `StrictUndefined` makes rendering fail on undefined variables |
| Answers file validity | Validator |

Not adopted: semantic contradiction detection (not deterministic), JSON Schema for answers (duplicates Copier validators and adds a dependency), markdownlint and a separate link checker (extra tools; the validator covers relative links), per-commit linting (redundant under squash merge), pre-commit-hooks (the validator already detects conflict markers). `pre-commit` itself is optional and runs the same validator.

Rule wording uses direct instructions ("Do X") with a reason where it is not obvious.

## GitHub plan constraint

The owner's account is on GitHub Free. Rulesets are enforced on public repositories only. For this public template, `template-ci` can be a required check. For private generated repositories, `protect-main` and required checks are shown but not enforced: the `governance` workflow still runs and reports, but a failing check does not block merging. The prohibitions in `AGENTS.md` (no commits to `main`, no merging) remain the only control there. Revisit if the plan changes.
