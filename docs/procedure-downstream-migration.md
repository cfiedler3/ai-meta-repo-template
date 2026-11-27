# Procedure: Migrating Existing Repositories

Bring a repository created before Copier (by the GitHub template flow or by hand) under Copier management. **Running this procedure on any repository requires separate owner authorization per repository.** This document is the plan; it changes nothing by itself.

## 1. Strategy

- Migrate one repository per pull request, on branch `chore/adopt-template-v1`.
- Order: a low-risk public repository first; then private repositories; `-private` repositories last, after a data-handling review.
- Copier has no adopt command in 9.19 (an upstream proposal exists but is not released). Adoption is a fresh `copier copy` over the existing repository, followed by manual reconciliation.
- After adoption, the repository updates with `procedure-update-and-profile-change.md` like any other.

## 2. Inventory (once, before the first migration)

Record for each `ai-` repository: Project ID, visibility, GitHub plan enforcement (rulesets enforce only on public repositories on GitHub Free), current `AGENTS.md` sections marked **[project]**, local copies of `standard-*.md`, and the intended profile and `efficiency_routing` value.

## 3. Per-repository steps

1. Clean tree on the default branch; `git switch -c chore/adopt-template-v1`.
2. Write `answers.yml` from the inventory (format: `procedure-provisioning.md`, Section 3). Move the `[project]` paragraph of the old `AGENTS.md` into `purpose` and `scope` only if it fits one sentence each; otherwise reconcile it in step 5.
3. Save the old governance for reference: `git show HEAD:AGENTS.md > /tmp/old-AGENTS.md` (outside the repository).
4. Render over the repository:

   ```
   copier copy --defaults --overwrite --data-file answers.yml --vcs-ref v1.0.0 gh:cfiedler3/ai-meta-repo-template .
   ```

5. Reconcile:
   - Move the old project sections (Project, Conventions, Data Handling fields, repository layout notes worth keeping) into the new `## Project` section.
   - Restore project files the render replaced: `README.md` (`git checkout HEAD -- README.md`), any project lines in `.gitignore`, and project-specific pull request template content.
   - Delete local copies of `docs/standard-*.md`; the new `AGENTS.md` links to pinned versions.
   - Agentic or multi-agent: create `docs/agent/state.md` when the first delegation is granted.
6. Run `python scripts/check_governance.py`; 0 errors.
7. Review the full diff against the old governance. List every rule whose meaning changed in the pull request body (ADR 0002 has the mapping).
8. Commit `chore(template): adopt ai-meta-repo-template v1.0.0` and open a pull request. The owner merges.
9. Owner settings: add the `governance` required status check to `protect-main`; confirm connector access is unchanged; update the assistant project instructions if the bootstrap rules changed (`standard-project-instructions.md`).

## 4. Rollback

Before merge: close the pull request. After merge: revert the squash commit. Nothing reaches `main` without review.

## 5. Checklist per repository

- [ ] Owner authorized migration of this repository
- [ ] Clean tree; dedicated branch
- [ ] Answers reviewed by the owner (profile, visibility, efficiency routing)
- [ ] Project-owned content moved into `## Project`; nothing silently dropped
- [ ] `README.md` and project `.gitignore` lines restored
- [ ] Local `standard-*.md` copies deleted
- [ ] `-private`: `data/` ignored; Data Handling section complete; no sensitive content in the diff, commit message, or pull request body
- [ ] Governance check: 0 errors
- [ ] Changed rule meanings listed in the pull request
- [ ] Required status check `governance` added to `protect-main`
- [ ] Connector access unchanged; assistant project instructions updated if needed

## 6. Change Log

| Date | Change |
|---|---|
| 2026-11-27 | Initial version. Execution not authorized |
