# Standard: Assistant Project Instructions

Defines what an assistant's project settings (the per-project instruction field in a chat assistant) contain for a repository created from this template. Scope: `ai-` repositories. `hm-` projects have no repository and are out of scope.

## 1. Principle

`AGENTS.md` is the source of truth. Project settings hold a pointer to the repository plus the minimum needed to bootstrap a session that has not yet read it. Nothing in `AGENTS.md` is copied into project settings; drift between two authorities is the failure this standard prevents.

## 2. Required sections

1. **Identity** — one paragraph: Project ID, what it is, backing repository (`<owner>/<project-id>`), local clone location, primary development tool.
2. **Start of every session** — attach and clone the repository; read `AGENTS.md`; attach and clone every repository listed as `enabled` in its Optional Modules table as a sibling at `../<module-repo>`; read any project documents `AGENTS.md` names; check history and open work before proposing changes.
3. **Rules that hold before the repository is read** — the autonomy limits from `AGENTS.md` §4 that must bind even on a cold session: per-action approval for repository changes, no direct commits to `main`, no unrequested tooling.
4. **Environment reality** — what the session's runtime can and cannot do (for example, no access to a desktop-only tool), and how work needing the unavailable tool is handed back.
5. **Working style** — the project's brief communication preferences.

## 3. Rules

- Keep it short. If a section grows past a screen, the content belongs in the repository.
- The Project ID appears verbatim and matches the repository name and local folder (see `standard-naming-project.md`).
- Every repository the session must attach — the project repository and each enabled module — must be granted to every assistant integration the owner uses (chat connector and coding-agent app are separate installations with separate repository access lists). Grant access at repository creation.
- When `AGENTS.md` changes in a way that affects bootstrap (new module, renamed document), update project settings in the same change.

## 4. Template
