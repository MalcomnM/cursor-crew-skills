---
name: setup-crew
description: "Place Cursor crew roles, the AGENTS.md crew block, and docs/agents into this project. Run once after installing cursor-crew-skills."
disable-model-invocation: true
---

# Set up the Cursor crew

The skills CLI copies this folder and stops there. It does not place `.cursor/agents`, the crew block in `AGENTS.md`, or `docs/agents`. This skill does that placement for the project you are in.

Run it once per project, from the project root. Python 3.9 or newer is enough. The copy step is the bundled script, so the bytes do not depend on how the agent reads this file.

## 1. Copy the bundled files

The skill directory is the folder that contains this `SKILL.md`. From the project root, preview, then apply:

```bash
python3 <skill-dir>/scripts/copy_assets.py --target <project-root> --dry-run
python3 <skill-dir>/scripts/copy_assets.py --target <project-root>
```

Completion: the command prints JSON. `mode` is `dry-run` or `apply`. A second apply prints an empty `changes` object.

The script writes only these paths:

- `.cursor/agents/grok-architect.md`, `grok-builder.md`, `grok-debugger.md`, `grok-prototyper.md`, `grok-researcher.md`, `grok-reviewer.md`, `grok-shipper.md`
- `AGENTS.md`, inserting the crew block between `<!-- BEGIN GROK CURSOR CREW -->` and `<!-- END GROK CURSOR CREW -->`
- `docs/agents/PROJECT.md`, `docs/agents/WORKFLOW.md`, `docs/agents/SKILL-ROUTING.md`

Read `conflicts` and `skipped` in the JSON before editing anything yourself.

- A path in `conflicts` already differed from the bundled role file. Leave that file as it is and tell the user the path. Exit code 2 means at least one role was left unchanged. The other copies still apply.
- A path in `skipped` already existed under `docs/agents/`. Leave that file as it is.
- Text outside the crew markers in `AGENTS.md` stays. A later run replaces only the marked block.

## 2. Ask for the project settings

Ask one question at a time. Lead with the recommended answer so a one-word confirmation is enough. Record the user's words. Leave every field they have not answered as `UNCONFIGURED`.

1. **Tracker.** Where issues for this repo live (GitHub Issues, local markdown, or another tracker they name). Recommended when `git remote` points at GitHub: GitHub Issues.
2. **Labels.** The labels they already use for work that is ready for an agent, needs info, or is out of scope. Recommended: keep the labels already on the tracker; do not create labels in this step.
3. **Branch names.** Stable branch, integration branch, and feature pattern. Recommended: `main`, `develop`, and `feature/[ticket]`.
4. **Test commands.** The commands that install, lint, typecheck, test, and build. A command that does not apply is `NOT_APPLICABLE` plus the user's reason.

Completion: each of the four answers is either a confirmed value or an explicit skip the user asked to leave `UNCONFIGURED`.

## 3. Fill PROJECT.md

Edit `docs/agents/PROJECT.md` in place. If the copy step skipped it, edit the existing file and keep its other sections.

Write the four answers into the matching rows: tracker, labels (note them in the tracker row or the setup-gaps section), stable branch, integration branch, feature pattern, and the install, lint, typecheck, test, and build rows.

Set the status line to `Status: BLOCKED` until the user has confirmed tracker, labels, branch names, and test commands in this session. After that confirmation, leave an existing stronger status as it is. While any of the four is still unconfirmed, the status line stays `BLOCKED`.

Completion: the status line is `BLOCKED`, or the user confirmed all four settings and the file already recorded them.

## 4. Stop at the working tree

Leave git remotes, tags, releases, and branch settings untouched. Do not push, fetch, switch branches, or edit branch protection. Tell the user which files were written, which conflicts or skips remain, and that `PROJECT.md` stays `BLOCKED` until they confirm the four settings.
