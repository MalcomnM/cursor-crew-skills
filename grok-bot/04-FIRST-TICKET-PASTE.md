# First ticket prompt

Replace the ticket and change description, then paste into Foreman.

```text
Run this ticket through the Cursor crew:

Ticket: REPLACE_WITH_TICKET_ID
Change: REPLACE_WITH_REQUESTED_BEHAVIOR
Acceptance criteria: REPLACE_WITH_OBSERVABLE_OUTCOMES

Use the configured repository, project workflow, and SKILL-ROUTING.md. Have Builder load tdd, Reviewer load code-review independently, and the PR author load pr. Report the loaded skills and library revision. Check PROJECT.md is READY. Clarify missing product decisions before implementation, and record the agreed test interfaces. Use one Builder and one feature branch named feature/[ticket], starting at the latest develop.

I authorize implementation of this ticket, tests, commits and pushes to its feature branch, a PR targeting develop, independent review, and Reviewer/Merger squash-merging the approved green PR into develop. I authorize Foreman and Reviewer/Merger to exchange briefs and results for this task and dispatch the necessary Cursor jobs. Do not merge to main, deploy, close the issue, or create recurring jobs.

Keep me updated when the feature is built, when review requests changes, and when it is integrated or blocked. Return the feature PR, squash commit, check evidence, and a short description of the resulting behavior. If an existing run or PR already owns this ticket, reconcile and resume it rather than starting a duplicate.
```
