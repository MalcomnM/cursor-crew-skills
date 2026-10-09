---
name: crew-gitflow
description: Run an opted-in Cursor crew project's feature-ticket, develop, and main workflow with Matt Pocock skills, independent review, squash feature integration, and approved releases.
---

# Crew Git Flow

Read the target project's docs/agents/PROJECT.md, WORKFLOW.md, and SKILL-ROUTING.md. If the project has not adopted the crew, explain the setup path; do not impose its branch policy on unrelated repositories. Bundled references provide the starter policy when preparing setup: [workflow](references/WORKFLOW.md) and [skill routing](references/SKILL-ROUTING.md).

Identify role, action, repository, exact refs, spec version, authority, and return destination from the current brief. Use the assigned role in `.cursor/agents/` or the installed cursor-crew plugin. Foreman owns the ledger; Reviewer/Merger owns integration.

Select the actual upstream skill for the job: tdd and codebase-design for implementation, code-review for independent review, diagnosing-bugs for diagnosis, research for reading, prototype for experiments, and pr for PR bodies. Preserve their reference files and load them when directed. For automatic crew planning use crew-plan; for architecture use crew-architecture. Upstream manual-only commands remain manual.

Build on feature/[ticket] from develop. Review exact commits and the combined candidate. Squash features into develop. Promote develop to main by user-approved merge commit, then synchronize main back. SKILL-ROUTING.md documents adaptations of upstream branch, review, report-location, and closure behavior.

Report checks, evidence, used skills, library revision, and the actual result. Reconcile prior attempts before retrying. Missing required verification or authority is BLOCKED, not success.
