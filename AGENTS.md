# AGENTS.md

Cross-tool governance for this repository. Any AI coding agent or assistant working here reads this file first. Tool-specific instruction files (for example `CLAUDE.md`) import this file and add nothing of their own.

This file was created from `ai-meta-repo-template`. Sections marked **[project]** are completed by the project; everything else applies to every repository created from the template and is changed only in the template.

---

## 1. Project

**[project]** One paragraph: what this repository is, who it is for, and what "done" looks like.

- **Project ID:** `<project-id>` — see `docs/standard-naming-project.md`
- **Backing:** `ai-` (this repository is the source of truth)
- **Visibility:** private | public — verify in repository settings; the name does not establish it

---

## 2. Source of Truth

- This repository is the authoritative record for the project. Durable decisions, constraints, and conventions are recorded here, not in chat history or assistant project settings.
- Assistant project settings hold only a pointer to this repository and context that does not belong in version control.
- Standards are linked from `ai-meta-repo-template/docs/`, never copied into this repository.

---

## 3. Core Principle

AI systems are collaborators, not autonomous agents. Every change to this repository requires explicit human authorization at each step. When in doubt about whether an action needs confirmation, the agent asks.

Behavioral foundation:

1. Don't assume. Don't hide confusion. Surface trade-offs.
2. Minimum change that solves the problem. Nothing speculative.
3. Touch only what you must. Clean up only your own mess.
4. Define success criteria before starting. Loop until verified.

---

## 4. Autonomy Limits

### Permitted without confirmation

- Reading any file in the repository
- Generating content for review within the conversation
- Suggesting changes, improvements, or options
- Drafting pull request bodies for human review

### Requires explicit confirmation in the current session

- Creating a branch
- Committing or pushing to any branch
- Opening a pull request
- Any other action that modifies repository state

Approval is per action and per session. It does not carry over.

### Prohibited

- Committing directly to `main` under any circumstances
- Merging pull requests
- Deleting branches, files, or history
- Creating, rotating, or storing credentials; committing secrets
- Modifying repository, governance, or security settings
- Any irreversible action without human approval

---

## 5. Branch and Commit Rules

1. All changes go through a branch and a pull request. `main` is protected by a ruleset that enforces this.
2. Branch names: `<type>/<short-description>` using the commit types below (for example `docs/naming-standard`, `feat/export-script`). **[project]** may add project-specific types.
3. Commit messages follow Conventional Commits: `type(scope): summary`. Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`.
4. One logical change per pull request. Pull requests are squash-merged.
5. Do not rewrite published history. Force pushes are blocked on `main`.
6. Multi-file changes are committed atomically (one commit, all files), not file by file.

---

## 6. Pull Requests

- Every pull request uses `.github/pull_request_template.md`. GitHub applies it automatically for pull requests opened in the web UI; pull requests opened through the API do **not** inherit it, so an agent must reproduce its sections in the body.
- Pull request bodies use real line breaks, never literal `\n` escape sequences.
- The governance confirmation checklist in the template is always completed.

---

## 7. Working Practices

- Read this file and the project README before making changes.
- Do not add tools, frameworks, dependencies, or processes unless their long-term value clearly exceeds their maintenance cost; say so in the pull request.
- Prefer editing an existing file over creating a parallel one. Prefer small, verifiable changes.
- When a task is ambiguous, ask one question rather than guessing, unless a wrong guess is cheap to undo.
- Keep documentation current with the change that affects it, in the same pull request.
- Never load binary or media file content (images, video, audio, archives, executables) into model context. Run deterministic extractors and pass only their text output. For large text files, extract the relevant section first.
- Worker agents never inherit the session model; every delegated task names a cheaper model explicitly.

---

## 8. Optional Modules

| Module | Status | Reference |
|---|---|---|
| Efficiency routing | enabled | `<projects-root>/ai-code-efficiency/AGENTS.md` |

A module is enabled when its status reads `enabled`; the agent reads the reference before starting work. Set `disabled` to turn it off. `<projects-root>` is the machine's projects folder; the reference is a sibling clone, not a copy inside this repository. References become URLs when the module repository is public.

---

## 9. Repository Layout

```
.
├── .github/
│   └── pull_request_template.md
├── AGENTS.md           this file
├── CLAUDE.md           imports AGENTS.md
├── LICENSE
├── README.md           project overview and usage
└── docs/               design notes, decisions, references
```

**[project]** Extend this tree as the project grows. Keep it accurate.

---

## 10. Conventions

**[project]** Language, formatting, test, and build conventions specific to this project. Delete the section if there are none.

---

## 11. Related Standards

- `docs/standard-naming-project.md` — project identity and naming
- `docs/standard-naming-github.md` — GitHub-specific repository rules

In repositories other than the template, these are links to `ai-meta-repo-template`, not local files.
