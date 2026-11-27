# 0001. Adopt Copier for provisioning and updates

- Date: 2026-11-27
- Status: accepted (owner decisions D1, D2, D9, D14, D15, D16)

## Context

Repositories were created with GitHub's template-repository copy, then edited by hand through eight manual steps. Nothing updated them afterwards ("apply changes forward when touching each one"), so governance drifted. Requirements: interactive and unattended initialization, profile selection, validated names, deterministic output, recorded versions, updates of existing repositories, profile changes in place, no servers, Windows and Linux.

Options considered: GitHub template repositories (one-shot copy, no updates), Cookiecutter with cruft (two tools for what Copier does natively), Yeoman (generator code to write and maintain), Backstage software templates (needs a server), projen (project configuration as code, aimed at JS/TS projects).

## Decision

1. Use Copier (minimum 9.13.0, tested with 9.19.1) and only its native features: typed questions with validators, conditional files and content, the answers file, Git-tag versions, `copier update` three-way merge, `copier update --data` for answer changes, `copier recopy`, and `copier check-update`.
2. `_subdirectory: template`: everything a generated repository receives lives in `template/`. The repository root (this repository's own `AGENTS.md`, standards, procedures, tests) is never rendered.
3. No `_tasks`, `_migrations`, or `_jinja_extensions` in v1. Copier then never needs `--trust`, never runs code from the template, and never runs anything again on update. `git init` and `gh repo create` stay explicit steps; publication keeps its separate owner approval.
4. `.gitattributes` with `* text=auto eol=lf` in this repository and in generated repositories, so Windows line endings cannot create spurious update conflicts.
5. Releases are SemVer tags created by the owner after merge; a change in meaning of a rule is a major release. The first release after this change is `v1.0.0`.
6. After `v1.0.0`, the GitHub "template repository" flag is turned off so Copier is the only provisioning path. **Use this template** would otherwise copy this maintenance repository, not a project.

## Consequences

- Provisioning needs Python and Copier where it runs; generated repositories need only Python for the validator.
- Updates need the template (remote or a local clone) and a clean Git tree; daily work never does.
- A future change that needs code at update time (for example moving files between layouts) requires a new decision record before adding `_migrations`.
