# Crew project configuration

Status: BLOCKED — see Setup gaps. Repository, branch policy, and check commands are verified; Bot identities, Cursor connection, tracker reconciliation, and branch protection are not.

Foreman fills this file during bootstrap from verified project information. READY requires repository access, Cursor launch or a documented manual path, actual check commands, merge policy, and a durable result location. Do not dispatch implementation while required fields remain UNCONFIGURED.

## Purpose

This repository is the Cursor Crew Skills library itself: 27 byte-for-byte preserved Matt Pocock skills (plugins/matt-pocock-skills), three crew skills and seven Cursor roles (plugins/cursor-crew), the project installer and validator (scripts/), project templates (templates/project), and Grok Bot paste prompts (grok-bot/). It is also an opted-in crew project, so its own changes follow WORKFLOW.md.

Library sources live under plugins/ and templates/. The copies under .cursor/ and docs/agents/ are installer output pinned by .cursor/crew-lock.json; change the sources, then refresh the copies in a separate reviewed configuration change. Never edit files listed in upstream-lock.json except through the reviewed upstream update in docs/UPSTREAM.md.

| Setting | Value |
|---|---|
| Repository URL and provider | https://github.com/MalcomnM/cursor-crew-skills (GitHub, public) |
| Git remote | origin |
| Stable branch | main (provider default branch) |
| Integration branch | develop |
| Feature pattern | feature/[ticket] from develop |
| Feature merge method | squash into develop, one ticket commit |
| Release merge method | merge commit, develop into main, after explicit user approval |
| Main synchronization | after each release, sync main back into develop: fast-forward develop when possible; otherwise reviewed main-to-develop merge PR |
| Foreman Bot identity | UNCONFIGURED |
| Reviewer/Merger Bot identity | UNCONFIGURED |
| Cursor connection / manual launch path | UNCONFIGURED; Cursor Cloud Agents can read and push this repository (verified by ticket crew-setup) |
| Cursor Cloud environment | UNCONFIGURED; Python 3.9+ and Git only, no install step |
| Cursor worker model | inherit configured parent model; record actual choice at setup |
| Tracker / ticket source | UNCONFIGURED; GitHub Issues is enabled with only default labels; repository specs are acceptable |
| Ticket-to-branch mapping | ticket key used literally, e.g. crew-setup -> feature/crew-setup |
| Spec and acceptance source | UNCONFIGURED; per-ticket brief until a tracker is chosen |
| Durable task ledger | UNCONFIGURED; tracker preferred; otherwise Foreman-owned attached Markdown |
| Install command | NOT_APPLICABLE; standard-library Python only, no dependencies |
| Typecheck command | NOT_APPLICABLE; no type checker is configured |
| Lint command | NOT_APPLICABLE; no linter is configured (scripts/validate.py covers structural checks) |
| Test command | `python3 scripts/validate.py` then `python3 -m unittest discover -s tests -v` |
| Build command | NOT_APPLICABLE; nothing is built or packaged |
| Browser / integration checks | NOT_APPLICABLE; plugin discovery and Bot dispatch require a manual account test |
| Agreed test interfaces or source | scripts/install.py CLI and plan/apply functions (tests/test_install.py); scripts/vendor_upstream.py (tests/test_vendor.py); scripts/validate.py exit status |
| Required provider CI checks | Workflow "Validate skills library" (.github/workflows/validate.yml), job validate, runs on pull_request and on push to main/develop; whether it is a required check is UNCONFIGURED |
| PR approval requirements | UNCONFIGURED; branch protection is not readable by the worker token |
| Develop merge queue / concurrency control | UNCONFIGURED; no merge queue observed |
| Branch protections observed | No repository rulesets; classic branch protection unreadable (HTTP 403). Squash, merge commit, and rebase merges are all enabled; delete_branch_on_merge is off |
| Effects of updating main | Runs the validate workflow only; no deployment environments or release automation. Tags (existing: v0.1.0) and releases are created only with explicit scope |
| Skills library source | https://github.com/MalcomnM/cursor-crew-skills (this repository) |
| Skills library revision | Read .cursor/crew-lock.json; installed from cf45066ae0720a173745d64a310324c60cf79c98, upstream 49dd158d1076134a641b33efb035946536778336 |
| Skill routing | docs/agents/SKILL-ROUTING.md |
| Upstream tracker/domain setup | UNCONFIGURED; reconcile issue-tracker.md, domain.md, triage-labels.md through setup-matt-pocock-skills |
| Artifact/report storage | Cursor job report + linked tracker or PR; verify access |
| Initial parallel builders | 1 |
| Maximum automatic repair cycles | 2 per ticket, then report |
| Feature integration authority | Only for tickets whose brief explicitly permits integration |
| Release authority | Explicit user approval of source SHA, target SHA, and known deployment consequence |
| Cleanup authority | Only when task brief explicitly lists or authorizes merged feature cleanup |

Credentials belong in the supported secrets mechanism, never in this file. Keep task-specific approvals in the task record rather than converting them into permanent authority here. Record any temporary capability gaps and their owner below.

## Setup gaps

- Foreman and Reviewer/Merger Bot identities, and the Cursor connection or manual launch path: owner Foreman during Grok Bot setup.
- Tracker, durable task ledger, and setup-matt-pocock-skills reconciliation (issue-tracker.md, domain.md, triage-labels.md): owner Foreman, with the user's tracker choice.
- Branch protection for main and develop (required PR review, required "validate" check, no force-push or deletion): owner repository admin; not readable by the worker token.
