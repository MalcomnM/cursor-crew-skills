# Release preparation and approval

Paste the preparation message into Foreman first. It prepares the release; it does not authorize updating main.

## Prepare

```text
Prepare a release from develop to main for the configured repository. Have Reviewer/Merger obtain an independent release review and verify the proposed combined result. Freeze and report the exact develop and main SHAs, included tickets, checks, migrations, known risks, and whether updating main triggers a deployment.

Prepare or update the release PR with base main and head develop. Do not merge, deploy, tag, or close issues. Show me the exact candidate to approve. Keep any subsequent feature integration from silently changing this release candidate; pause the merge queue while the release is awaiting my decision, or refresh the candidate and ask for renewed approval.
```

## Approve the reported candidate

Replace both SHA values from the prepared report. Add any deployment authorization deliberately if your existing CI deploys on main.

```text
Approve release of develop at REPLACE_WITH_DEVELOP_SHA into main at REPLACE_WITH_MAIN_SHA using a normal merge commit. Reviewer/Merger may perform that release merge after all recorded checks and required provider approvals pass, then synchronize main back into develop without rewriting history. If either head changes, re-prepare the candidate and return for approval. Do not create tags, close tickets, or perform a separate deployment.
```

If updating main automatically deploys, the approval must explicitly acknowledge that consequence before merging. If you instead want a squash release, ask Foreman to revise and review the repository workflow first, including how main and develop ancestry will be synchronized; do not select a different merge button ad hoc.
