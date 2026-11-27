# ai-meta-repo-template

Provisions and updates `ai-` repositories with [Copier](https://copier.readthedocs.io/). Each generated repository gets cross-tool agent governance (`AGENTS.md`) for one of three development profiles, a governance check, CI, and the MIT license.

| Profile | Use when |
|---|---|
| `assisted` | The owner directs the work; the assistant needs approval for each change |
| `agentic` | The owner delegates bounded work; the assistant stops at approval gates |
| `multi-agent` | Agentic, plus parallel specialist agents with independent review |

Profiles describe how a project is developed, not whether it uses AI. Details: [`docs/standard-governance-profiles.md`](docs/standard-governance-profiles.md).

## Create a repository

```
copier copy --vcs-ref vX.Y.Z gh:cfiedler3/ai-meta-repo-template <project-id>
```

Unattended: add `--defaults --data-file answers.yml`. Full steps, including publication and hosted sessions: [`docs/procedure-provisioning.md`](docs/procedure-provisioning.md).

## Update a repository or change its profile

```
copier update --defaults --vcs-ref vX.Y.Z
copier update --defaults --vcs-ref=:current: --data profile=agentic
```

Review, validate, and roll back: [`docs/procedure-update-and-profile-change.md`](docs/procedure-update-and-profile-change.md). Repositories created before Copier: [`docs/procedure-downstream-migration.md`](docs/procedure-downstream-migration.md).

## Repository layout

| Path | Contents |
|---|---|
| `copier.yml` | Questions, validators, settings |
| `includes/governance/` | Governance modules per layer and the manifest that defines profile inheritance |
| `template/` | Everything rendered into a generated repository |
| `docs/` | Standards, procedures, and decision records for this template |
| `tests/` | Acceptance tests, answer fixtures, and reviewed output snapshots |
| `AGENTS.md` | Governance for maintaining this repository (not rendered) |

## Changing the template

Follow `AGENTS.md`, Section 6. Run `python -m unittest discover -s tests -v` (needs Python 3.9+, Git, and Copier 9.19). The owner tags releases after merge; generated repositories pick changes up with `copier update`.
