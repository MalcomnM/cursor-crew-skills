# Cursor Crew Skills

A reusable library for Grok Bot coordination and Cursor engineering agents, maintained by MalcomnM. It includes 27 selected Matt Pocock engineering/productivity skills with their original references and invocation flags, plus three crew skills and seven Cursor roles.

This is a separate repository, not a GitHub fork. The upstream snapshot is [mattpocock/skills at 49dd158d1076](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336). Upstream content is preserved byte-for-byte; [NOTICE.md](NOTICE.md) and [upstream-lock.json](upstream-lock.json) record attribution and provenance. Experimental and miscellaneous skills are intentionally excluded.

## Install with the skills CLI

Node.js 22.20 or newer is what the skills CLI asks for. The CLI copies each selected skill folder into `.agents/skills`. It installs Matt Pocock's skills, `crew-plan`, `crew-gitflow`, `crew-architecture`, and `setup-crew`. It does not copy `.cursor/agents`, `AGENTS.md`, or `docs/agents`.

Install `setup-crew`, then run that skill in the project. The skill's helper copies the seven role files, merges the crew block into `AGENTS.md`, and copies `docs/agents` without replacing local edits.

```bash
npx skills@latest add MalcomnM/cursor-crew-skills --agent cursor --skill setup-crew -y
```

Omit `--skill` to pick skills interactively. Skill names are exact; the CLI does not expand globs. Details and the project-local installer are in [Installation and updates](docs/INSTALL.md).

## Start with a project

Clone this library outside your application repo, select a reviewed release, preview installation, then apply it on a configuration branch:

```bash
git clone https://github.com/MalcomnM/cursor-crew-skills.git
cd cursor-crew-skills
git checkout v0.1.0
python3 scripts/install.py --target /absolute/path/to/your-project
python3 scripts/install.py --target /absolute/path/to/your-project --apply
```

The installer makes project-local copies; it does not push, merge, install packages, change branch settings, or store secrets. It preserves existing project configuration and refuses to overwrite locally changed managed files. Commit the installed files so Cursor Cloud Agents can read the same revision. [Installation and updates](docs/INSTALL.md).

## Connect Grok Bot

Follow [START-HERE.md](grok-bot/START-HERE.md), then paste [Foreman](grok-bot/01-FOREMAN-PASTE.md), [Reviewer/Merger](grok-bot/02-REVIEWER-MERGER-PASTE.md), and [project setup](grok-bot/03-PROJECT-SETUP-PASTE.md). The setup reconciles Matt's issue-tracker, domain, and triage configuration. It does not assume that a desktop-only skill installation is visible in Grok Bot or a Cloud job.

## Use as Cursor plugins

In Cursor Customize, choose From GitHub Repository and enter this repository URL. Install both `matt-pocock-skills` and `cursor-crew`. The repository includes the marketplace and plugin manifests required for this flow. [Cursor repository import](https://cursor.com/docs/skills#installing-skills-from-a-repository).

Plugin installation supplies capabilities; the project installer/configuration supplies repository policy. Prefer one installation source for each skill name. For repeatable Cloud tasks, use project-local copies and the lock file; do not rely on desktop plugin availability propagating automatically.

## Roles and skills

| Role | Main skills |
|---|---|
| Foreman | crew-plan, grilling, domain-modeling |
| Builder | tdd, codebase-design |
| Reviewer | code-review, tdd, codebase-design |
| Shipper | crew-gitflow, pr |
| Debugger | diagnosing-bugs, tdd |
| Architect | crew-architecture, codebase-design |
| Researcher | research |
| Prototyper | prototype |

[Skill routing and adaptations](templates/project/docs/agents/SKILL-ROUTING.md) describes the manual daily commands as well as the crew's automatic paths. Original `implement-spec` and prototype branch assumptions do not replace an opted-in project's branch policy.

## Git policy for opted-in projects

- `feature/[ticket]` starts from `develop`.
- Independent review and required checks precede each squash merge into `develop`.
- `develop` releases to `main` by approved merge commit, followed by synchronization back to `develop`.
- Foreman owns scope and task status; Reviewer/Merger owns the serialized integration queue.

## Maintain the library

Use [UPSTREAM.md](docs/UPSTREAM.md) for reviewed upstream updates. Run `python3 scripts/validate.py` and `python3 -m unittest discover -s tests -v` before releasing. This repository's initial main/develop branches begin at the same published baseline. Future library changes can follow the same feature squash workflow.

The plugin manifests and installer are validated by repository checks. Actual plugin discovery, account permissions, and Bot-to-Cursor dispatch require your account's setup test; static validation does not claim marketplace approval or a live end-to-end Bot run.

License: MIT. Matt Pocock and other upstream credits remain with their respective files; this project does not imply endorsement.
