# Procedure: Template Updates and Profile Changes

Apply template changes to a generated repository, change its answers (including profile), and recover from a failed update. Every step uses native Copier and Git commands.

## 1. Versions

The template is released as SemVer tags. The owner creates them after merge.

| Change | Bump |
|---|---|
| Meaning of an existing common or profile rule changes; a file moves; an answer is renamed or removed | major |
| New rule, section, question with a default, or profile capability | minor |
| Wording, formatting, documentation, or fixes with no change in meaning | patch |

A repository's version is `_commit` in `.copier-answers.yml`. There is no other version record. Never edit that file by hand.

## 2. Ownership

| Class | Files | Update behavior |
|---|---|---|
| Template-controlled | `CLAUDE.md`, `.gitattributes`, `LICENSE`, `scripts/check_governance.py`, `.github/workflows/governance.yml`, `.pre-commit-config.yaml`, `docs/governance/*` | Replaced by the template; local edits are drift and fail the CI drift check |
| Jointly managed | `AGENTS.md` (template-owned sections plus the project-owned section), `.gitignore` (template lines plus project lines), `.github/pull_request_template.md` | Three-way merged; template-owned parts change, project parts are kept |
| Project-controlled | `README.md`, `docs/decisions/*`, `docs/agent/state.md`, all source code and other files | Never changed by an update. `README.md` and `docs/decisions/README.md` are created once and then skipped |

## 3. Check for an update

```
copier check-update
```

Exit status 2 means a newer release exists (`--output-format json` for scripts).

## 4. Update to a new release

1. Start from a clean working tree: `git status` shows nothing.
2. Create a branch: `git switch -c chore/template-update-vX.Y.Z`.
3. Preview: `copier update --defaults --pretend --vcs-ref vX.Y.Z`.
4. Apply: `copier update --defaults --conflict inline --vcs-ref vX.Y.Z`. Copier re-renders the old version with your recorded answers, applies the new version, and re-applies your changes.
5. Resolve conflicts. Search for conflict markers (`<<<<<<<`) and `*.rej` files, merge each by hand, and delete the markers and `.rej` files.
6. Review the full `git diff`. Confirm the `## Project` section of `AGENTS.md`, `README.md`, `docs/decisions/`, and `docs/agent/state.md` are unchanged.
7. Run `python scripts/check_governance.py`; it must report 0 errors. It fails on remaining conflict markers, `.rej` files, and placeholders.
8. Commit `chore(template): update to vX.Y.Z` and open a pull request. CI runs the governance check and the drift check.

## 5. Change the profile or another answer

Changing an answer does not change the template version when `:current:` is used, so the diff shows only the effect of the answer.

1. Agentic or multi-agent repositories: add an entry to `docs/agent/state.md` recording the change and its reason.
2. Clean tree; branch `chore/profile-<from>-to-<to>`.
3. Run:

   ```
   copier update --defaults --vcs-ref=:current: --data profile=<assisted|agentic|multi-agent>
   ```

4. Expect: the autonomy and profile sections of `AGENTS.md` change; `docs/governance/` files are added or removed; the pull request template's governance confirmation changes; project-controlled files, including `docs/agent/state.md`, are untouched.
5. Upgrading to agentic: create `docs/agent/state.md` before the first delegation.
6. Continue with steps 5 to 8 of Section 4, using the commit message `chore(profile): switch to <profile>`.

The same command changes any other answer, for example `--data efficiency_routing=true`. The `## Project` section is project-owned after creation; edit it directly instead of changing `purpose` or `scope`.

## 6. Roll back

| When | How |
|---|---|
| Before committing | `git reset --hard` then `git clean -d -i` (review what it deletes) |
| After committing, before merge | Close the pull request and delete the branch |
| After merge | Revert the squash commit with a new pull request; this also restores `.copier-answers.yml` |

## 7. Recover from a broken update

When the merge result is unusable, re-render the recorded version from scratch on a new branch, then restore project-owned content from Git:

```
copier recopy --defaults --overwrite --vcs-ref=:current:
git diff
```

Restore the `## Project` section and any project file from `git show HEAD:<path>`, then validate and commit as in Section 4. History is never rewritten.

## 8. When the template is unavailable

Generated repositories never depend on the template at run time. Governance, procedures, and the validator are local. Without the template you lose only updates and the CI drift check, which passes with a warning when it cannot reach the template. Standards links are pinned to the release you were generated from.

## 9. Change Log

| Date | Change |
|---|---|
| 2026-11-27 | Initial version (ADR 0001, ADR 0004) |
