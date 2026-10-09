# Crew project configuration

Status: UNCONFIGURED

Foreman fills this file during bootstrap from verified project information. READY requires repository access, Cursor launch or a documented manual path, actual check commands, merge policy, and a durable result location. Do not dispatch implementation while required fields remain UNCONFIGURED.

| Setting | Value |
|---|---|
| Repository URL and provider | UNCONFIGURED |
| Git remote | origin; verify during setup |
| Stable branch | main |
| Integration branch | develop |
| Feature pattern | feature/[ticket] |
| Feature merge method | squash |
| Release merge method | merge commit |
| Main synchronization | fast-forward develop when possible; otherwise reviewed main-to-develop merge PR |
| Foreman Bot identity | UNCONFIGURED |
| Reviewer/Merger Bot identity | UNCONFIGURED |
| Cursor connection / manual launch path | UNCONFIGURED |
| Cursor Cloud environment | UNCONFIGURED |
| Cursor worker model | inherit configured parent model; record actual choice at setup |
| Tracker / ticket source | UNCONFIGURED; repository specs are acceptable |
| Ticket-to-branch mapping | UNCONFIGURED; stable legal Git ref, e.g. ABC-123 |
| Spec and acceptance source | UNCONFIGURED |
| Durable task ledger | UNCONFIGURED; tracker preferred; otherwise Foreman-owned attached Markdown |
| Install command | UNCONFIGURED |
| Typecheck command | UNCONFIGURED or NOT_APPLICABLE with reason |
| Lint command | UNCONFIGURED or NOT_APPLICABLE with reason |
| Test command | UNCONFIGURED |
| Build command | UNCONFIGURED or NOT_APPLICABLE with reason |
| Browser / integration checks | UNCONFIGURED or NOT_APPLICABLE with reason |
| Agreed test interfaces or source | UNCONFIGURED; may be ticket-specific |
| Required provider CI checks | UNCONFIGURED; do not substitute invented names |
| PR approval requirements | UNCONFIGURED |
| Develop merge queue / concurrency control | UNCONFIGURED |
| Branch protections observed | UNCONFIGURED |
| Effects of updating main | UNCONFIGURED; includes automatic deployment |
| Skills library source | https://github.com/MalcomnM/cursor-crew-skills |
| Skills library revision | Read .cursor/crew-lock.json after project installation; record an exact commit for plugin installations |
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

UNCONFIGURED
