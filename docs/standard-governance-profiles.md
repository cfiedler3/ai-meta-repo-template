# Standard: Development Governance Profiles

## 1. Purpose

Define the development profiles a repository created from `ai-meta-repo-template` can use, what each one governs, and how their rules are layered. A profile describes how the project is developed and governed. It says nothing about whether the resulting software uses AI.

---

## 2. Profiles

| Profile | Who directs the work | Repository changes | Adds |
|---|---|---|---|
| `assisted` | The owner | Owner approval for each action, every session | — |
| `agentic` | The assistant, within a delegation the owner grants | Free within the delegation; owner approval at gates | Delegated authority, persistent state, recovery, escalation, completion criteria |
| `multi-agent` | An orchestrating assistant, within a delegation | As agentic | Orchestration, specialist roles, delegation tracking, independent verification, model selection, cost control |

Choose the lowest profile that fits. Use `multi-agent` only when work routinely splits into independent parallel tasks: multi-agent runs cost several times the tokens of a single agent, and coordination overhead can exceed the work itself.

---

## 3. Inheritance

```
common ──┬── assisted
         └── agentic ── multi-agent
```

- **Common** rules apply to every profile: authority and precedence, prohibitions, source control, working practices, references, and, when applicable, data handling and optional modules.
- **Assisted** and **agentic** each add exactly one autonomy section. They are mutually exclusive; no repository receives both.
- **Multi-agent** reuses every agentic section unchanged and adds its own. It never overrides an agentic rule.
- Inheritance is defined once, in `includes/governance/manifest.jinja`. The tests fail if a profile renders a section from a layer it does not inherit, or if multi-agent changes an agentic section.

---

## 4. Sections

Each generated `AGENTS.md` section heading carries an ownership marker. The section id starts with its layer code.

| Layer | Code | Sections |
|---|---|---|
| Common | `cmn` | `header`, `authority`, `prohibited`, `source-control`, `practices`, `data-handling` (`-private` only), `modules` (when enabled), `references` |
| Assisted | `ast` | `autonomy` |
| Agentic | `agt` | `autonomy`, `state`, `recovery`, `escalation`, `completion` |
| Multi-agent | `mag` | `orchestration`, `delegation`, `verification`, `models-cost` |

The project-owned section (`## Project`) is always last. Template updates never change it.

---

## 5. Approval gates (agentic and multi-agent)

Within an active delegation the assistant may branch, edit, run checks, and commit. It needs explicit owner approval, in the current session, for:

1. the first push of each branch;
2. opening a pull request;
3. any action outside the delegated scope;
4. any irreversible action;
5. any security or privacy uncertainty.

Without an active delegation, every repository-changing action needs approval, as in `assisted`. Merging pull requests and committing to `main` are prohibited in every profile.

---

## 6. Files by profile

| File | assisted | agentic | multi-agent | Owner |
|---|---|---|---|---|
| `docs/governance/agentic-operations.md` | — | yes | yes | template |
| `docs/governance/multi-agent-operations.md` | — | — | yes | template |
| `docs/agent/state.md` | — | created by the assistant before the first delegation | same | project |

The template never creates or deletes `docs/agent/state.md`, so it survives every profile change as a historical record.

---

## 7. Changing profile

Run the profile change procedure in `procedure-update-and-profile-change.md`. Never edit `profile:` in `.copier-answers.yml` by hand.

---

## 8. Change Log

| Date | Change |
|---|---|
| 2026-11-27 | Initial version: three profiles, inheritance model, section ids, approval gates (ADR 0002) |
