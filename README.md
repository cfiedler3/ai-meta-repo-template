# ai-meta-repo-template

Starting point for every `ai-` repository: agent governance (`AGENTS.md`), license, and the project and GitHub naming standards.

## Use

```
gh repo create <project-id> --template cfiedler3/ai-meta-repo-template --private --clone
```

or click **Use this template** on GitHub. Name the repository with its Project ID (see `docs/standard-naming-project.md`).

## After instantiating

1. `AGENTS.md` — complete every section marked **[project]**. Leave the other sections unchanged.
2. `README.md` — replace this file with the project's own.
3. `docs/` — delete `standard-naming-*.md`; link to them in this repository instead (see `docs/README.md`).
4. `AGENTS.md` Section 8 — set each optional module to `enabled` or `disabled`.
5. Add the repository to the assistant's GitHub connector.
6. Add a `protect-main` ruleset: require pull request, block force pushes, squash merge only.

## Contents

```
.
├── .github/
│   └── pull_request_template.md
├── .gitignore
├── AGENTS.md           cross-tool agent governance
├── CLAUDE.md           imports AGENTS.md
├── LICENSE             MIT
├── README.md
└── docs/
    ├── README.md
    ├── standard-naming-project.md
    └── standard-naming-github.md
```

## Changing the template

Rules in `AGENTS.md` sections not marked **[project]**, and the standards in `docs/`, are changed here only. Repositories created earlier are not updated automatically; apply changes forward when touching each one.
