# Cursor crew Git Flow

This policy uses three branch forms: main, develop, and feature/[ticket]. Feature PRs squash into develop. Releases merge develop into main with ancestry preserved. This is a simplified Git Flow, without mandatory release or hotfix branch families.

## Skill selection

Read SKILL-ROUTING.md for role-to-skill mapping and adaptations. Every job reports which skills it loaded and the library revision. Upstream skill content does not expand branch, tracker, merge, or deployment authority.

## Ownership and authority

Foreman in Grok Bot owns scope, decisions, dependency scheduling, and the task ledger. Reviewer/Merger in Grok Bot owns independent review and the single integration queue. Cursor workers execute one named role and return evidence.

Builder, Debugger, and Prototyper edit only their assigned feature branch. Researcher writes only assigned notes. Architect produces reports and proposals. Reviewer does not change source. Shipper integrates approved results and never changes behavior to make a merge work.

A task brief grants specific actions: read, build, push feature, open feature PR, review, integrate feature, prepare release, or release. A review request alone does not grant merge authority. Provider-required human approval remains required even after an AI verdict. Source-control access is not itself authorization to mutate anything accessible.

## Branch contract

| Branch | Purpose | Allowed incoming change |
|---|---|---|
| main | Stable released history | Approved release merge from develop |
| develop | Integrated work for the next release | Reviewed feature squash; controlled main synchronization |
| feature/[ticket] | One ticket in an isolated checkout | Commits for that ticket and merges of develop to update it |

Use the ticket key literally when it is a valid Git branch suffix. Otherwise record a stable sanitized mapping in the brief and validate with git check-ref-format --branch. Do not use literal brackets. No feature-to-main PRs. No feature merge commits or rebase merges into develop. No long-lived integration/* branches. A prototype also uses feature/[ticket], marked prototype-only, and does not integrate unless the user separately approves production scope and normal implementation review.

Do not reset or force-push published branches. To update a published feature, merge the latest develop into it, resolve its conflicts as the implementation owner, rerun checks, and obtain a fresh review. Do not keep developing on a branch after it has been squash-merged; create the next ticket from the new develop tip.

## Task record and handoff

Every job gets these fields, with real values rather than the angle-bracket examples:

```text
Task: <ticket ID and attempt number>
Role: <builder | reviewer | shipper | debugger | architect | researcher | prototyper>
Action: <allowed action>
Repository: <remote URL>
Environment: <Cursor job/environment or isolated checkout>
Branch: <feature/TICKET, develop, or main>
Source SHA: <full SHA for review/merge, or pending for a new build>
Base branch and SHA: <develop and SHA; main and SHA for release>
Spec/ticket: <accessible pointer and version>
Acceptance: <criteria or exact pointer>
Test interfaces: <agreed public interfaces or pointer>
Checks: <commands/config pointer>
Skills: <names, applicable references, library revision>
Related artifacts: <accessible notes, logs, prototype refs>
Authority: <feature push/PR/integration or specific release approval>
Return to: <Foreman or Reviewer/Merger identity and result location>
```

The current ledger is authoritative for stage and ownership. Typical stages are READY, BUILDING, REVIEWING, CHANGES-REQUESTED, MERGE-READY, INTEGRATING, INTEGRATED, RELEASE-READY, and RELEASED. BLOCKED and NEEDS-DECISION pause the relevant transition. INTEGRATED-CHECKS-FAILED stops the merge queue.

Only Foreman advances the ledger from reports and observed state. Include job IDs, PR URL, checked SHAs, spec revision, command results, review verdict, integration SHA, and release approval. Before retrying, inspect the existing job, PR, and remote branch. Resume an existing task instead of duplicating it after a timeout.

## Build one ticket

1. Read the brief, PROJECT.md, spec, glossary, ADRs, and role file. Confirm the actual remote URL and permissions.
2. Fetch the configured remote. Verify a clean, isolated checkout; preserve any existing work. Create feature/[ticket] from the latest remote develop. If the branch already exists, inspect task ownership and resume it only when it belongs to this assignment.
3. Run the baseline checks. Report pre-existing failures; do not suppress them. Pin agreed public test interfaces before behavior changes.
4. Implement one behavior slice at a time: failing regression/behavior test, minimal implementation, focused check, then the next slice. Test externally observable behavior rather than private implementation details. Documentation-only changes use appropriate validation instead of artificial tests.
5. Run the required checks and compare against every acceptance criterion. Keep unrelated work in follow-ups. Push only the assigned feature branch when authorized; open/update its PR with base develop.
6. Return source/base SHAs, actual check evidence, scope, risks, and the PR. DONE here means ready for review, not integrated.

Dependent tickets start after their prerequisite's squash commit is in develop. Do not stack new feature work on another feature's unsquashed commits. Separate parallel workers by environment or checkout and coordinate test ports/databases if infrastructure is shared.

## Independent review

Review takes a fixed feature SHA H, current develop SHA B, and spec revision S. A fresh job performs two passes: documented standards, and requested behavior. Keep their findings separate. An explicit spec pointer in the brief wins over guessed issue references. Cite file/hunk and the violated rule or requirement. Label design suggestions as judgments rather than undocumented rules.

Review the feature diff with git diff B...H and inspect the actual result of applying H to B in disposable verification storage. The proposed merged tree, not only the feature's old branch state, must pass all required checks. For releases, review the develop-versus-main change and the exact candidate merge result.

readonly: true in a subagent restricts writes and state-changing shell commands. Do not remove that restriction to run tests. Have the parent or a dedicated verification job prepare disposable files, run commands, and return immutable-SHA logs; Reviewer inspects that evidence and reports what it did not execute itself. A top-level Cloud task reading the role file must still observe the same no-source-edit policy.

Verdicts:
- APPROVE: requirements met, no blocking documented violations/bugs, required checks green.
- FIX-THEN-MERGE: bounded findings with concrete remedies.
- REWORK: scope or design needs substantial change.
- UNVERIFIED: required checks or evidence unavailable; never eligible to merge.

Bind approval to (repository, PR, H, B, S, checked tree, checks). Changes to the source, target, spec, required checks, or conflict resolution invalidate it. Reviewer never fixes its own findings. Foreman sends fixes to the implementation owner and commissions another review. Stop automatic fix loops after the configured limit.

## Squash a feature into develop

Prefer the source-control provider's PR squash operation with required checks and approvals enforced. Select the method explicitly. Re-fetch/re-read refs and confirm the reviewed head H and target B immediately before merging. Use provider head/base guards or a merge queue that verifies the current candidate. A guard on H alone does not guard B. Where the provider cannot guard B, coordinate a real exclusive merge window; if other writers cannot be excluded, return BLOCKED instead of claiming the race is safe.

Use a single merge owner and process one candidate at a time. After another feature lands, later candidates require fresh target-aware review/verification. Never use admin bypass to force a merge. If PR approval must come from another human account, report that exact pending gate.

The resulting commit has one parent, the previous develop tip, and a message naming the ticket, e.g. feat(exports): add CSV export (ABC-123). Preserve the PR URL and source SHA in the PR/report. Close or resolve the ticket only when separately authorized.

If the provider operation is unavailable, prepare the following candidate in a disposable checkout. Publishing this candidate is allowed only when PROJECT.md and the brief explicitly permit direct develop updates and all required protections are satisfied; otherwise return the prepared result and BLOCKED. This is not a branch-protection bypass.

1. Start the disposable checkout at verified B, with no uncommitted work. Validate the feature head still equals H.
2. Run git merge --squash H. A squash stages the combined tree without creating a merge commit. If it conflicts, abandon this disposable candidate and return it to the Builder. Do not use git merge --abort as squash cleanup: squash does not record MERGE_HEAD.
3. Run all required checks. If they fail, preserve logs and discard only the disposable candidate. Do not commit or publish a red result. Do not reset a user's checkout.
4. Inspect staged/unstaged output after checks; exclude generated files and unintended changes. The committed tree must be the reviewed and tested tree. If checks or formatting changed source, return for review. Commit one ticket change with parent B.
5. Recheck H and the remote target. Attempt only a normal non-force push to develop. If develop advanced or the push is rejected, fetch the new B and restart review/verification; never force the old candidate through. Use the same exclusive-window requirement to prevent source changes during this operation.

After the provider reports merged, verify its merge method and resulting squash SHA, and run/observe the required post-merge checks for that resulting commit. If the target has advanced, inspect that commit and its checks explicitly rather than attributing another commit's CI to it. On post-merge failure, stop the queue, report INTEGRATED-CHECKS-FAILED, and prepare a reviewed revert or repair; never rewrite develop.

Record integration before optional cleanup. A squash does not make feature commits ancestors of develop. Do not use git branch --merged alone for deletion. Verify the merged PR's exact head, squash result, no newer remote feature commits, no local unpushed commits, and a clean unused worktree. Delete only explicitly authorized feature branches/worktrees. If identity or ownership is uncertain, retain them and report it.

## Release develop to main

Prepare a PR with base main and head develop, but pause the feature integration queue while final release approval is pending. Capture main M and develop D. main must be an ancestor of D before release. If it is not, reconcile approved main history into develop through a separately reviewed synchronization first; do not reset either branch.

Review the release scope, migrations, compatibility, check evidence, and CI/deployment consequences. Test the exact proposed result. Ask the user to approve D into M and any automatic deployment consequence. Permission to build or integrate features does not authorize main. Changed D or M invalidates release approval.

Use the provider's normal merge-commit method, not squash or rebase. Verify the candidate refs under the same concurrency controls as feature integration. The release merge R preserves M and D as parents and normally has the same tree as D after the ancestry check. Keep main protections, CI, and required human approvals intact.

After the release, synchronize main back into develop. If develop is still D, fast-forward it to R through a provider-supported protected update when allowed. If direct fast-forward updates are blocked or develop has advanced, open a main -> develop synchronization PR and use a normal merge commit with required checks/review. This is an explicit exception to feature squash policy; it imports existing release ancestry and must not introduce unrelated production changes. Do not let source branch auto-deletion delete main or develop.

Record the release SHA, synchronization SHA, and verification results. If release succeeds but synchronization fails, report RELEASED with SYNC-BLOCKED and pause new integrations until reconciled. Do not retry the release or imply it was undone. Create tags, close issues, deploy separately, or announce a release only with explicit scope.

No standard emergency bypass is included. If an urgent main-only fix is needed, ask for a dedicated plan and authority, then reconcile it into develop before resuming normal releases.

## Result format

```text
Task / role / action:
Status: DONE | BLOCKED | NEEDS-DECISION | INTEGRATED | RELEASED | INTEGRATED-CHECKS-FAILED
Repository / PR / job:
Spec revision:
Source SHA / base SHA / checked tree:
Review verdict and findings pointer:
Checks: command, tested SHA/tree, exit result, evidence link
Resulting squash or release SHA:
Synchronization: SHA | not needed | SYNC-BLOCKED
Remaining decisions or follow-ups:
```

## Git reference

Git documents the difference between squash preparation and merge-commit operations, including squash not recording MERGE_HEAD. [git merge](https://git-scm.com/docs/git-merge). The workflow and approval conventions above are this project's chosen policy.
