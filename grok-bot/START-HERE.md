# Grok Bot and Cursor starter kit

Use Grok Bot for planning and coordination and Cursor Cloud Agents for repository work. This kit implements a simplified Git Flow with `main`, `develop`, and `feature/[ticket]`. The brackets are notation: ticket `ABC-123` uses `feature/ABC-123`.

Feature PRs always target `develop` and use squash merge, producing one commit per ticket. Releases go from `develop` to `main` by merge commit after your explicit approval. The release merge preserves ancestry between the two long-lived branches. This is the kit's recommended release default; change it deliberately if you want squash releases as well. There are no mandatory `release/*`, `hotfix/*`, or `integration/*` branches.

## What you will set up

- **Foreman**, a Grok Bot that talks with you, defines work, and dispatches Cursor jobs.
- **Reviewer/Merger**, a Grok Bot that commissions independent reviews and owns the merge queue.
- Seven Cursor roles: Builder, Reviewer, Shipper, Debugger, Architect, Researcher, and Prototyper. Shipper is the repository worker used by Reviewer/Merger; it is not another required Bot.
- Matt Pocock's 27 stable engineering/productivity skills, their supporting references and MIT license, plus crew-gitflow, crew-plan, crew-architecture, and project configuration. Experimental and miscellaneous upstream skills are excluded.

The paste messages configure the workflow only after you use them. The project installer changes files when called with --apply; it does not create Bots, remote branches, connectors, or permissions.

## Reusable library for new projects

The canonical reusable source is [MalcomnM/cursor-crew-skills](https://github.com/MalcomnM/cursor-crew-skills). Use its pinned project installer for repeatable Cloud Agent access, or import its marketplace and install both plugins in Cursor Customize. The public repository includes update and attribution instructions. See [06-SKILLS-AND-REUSE.md](06-SKILLS-AND-REUSE.md).

## 1. Create the two Bots

Sign in to Grok Bot using your Cursor account. Choose New, then Create new Bot. Create **Foreman**, then **Reviewer/Merger**. Name and edit each profile through its Bot menu. The documented setup uses a durable description plus task messages. [Bot setup](https://docs.x.ai/grok-bot/bots).

Open [01-FOREMAN-PASTE.md](01-FOREMAN-PASTE.md). Copy its profile description into Foreman's description, then paste its setup message into Foreman's chat. Do the same with [02-REVIEWER-MERGER-PASTE.md](02-REVIEWER-MERGER-PASTE.md).

In each setup message, select the other actual Bot with `@` where instructed. This gives each Bot a real recipient rather than merely a name. Bot handoffs are asynchronous; keep Foreman as the single task owner and Reviewer/Merger as the single merge owner. [Messaging](https://docs.x.ai/grok-bot/chat-and-collaboration).

## 2. Connect Cursor and your repository

Configure a Cursor Cloud Agent environment for the repository. Connect the source-control provider, install the project's dependencies, supply needed test secrets through supported secret controls, and verify that the application and required checks run. Cloud environments are separate from Grok Bot's shared computer and from your laptop. [Cursor setup and capabilities](https://cursor.com/help/ai-features/cloud-agents).

Ask Foreman to use its available Cursor connection to launch a small read-only task against the repository. Grok Bot's documented coding workflow delegates to Cursor through that connection. If your account does not expose it, use the manual fallback below; do not assume that mentioning Cursor establishes access. [Grok Bot and Cursor example](https://x.ai/bot/guides/grok-bot-101).

Set the worker model in Cursor to one available under your plan. The supplied subagents use `model: inherit`; their `grok-` names identify roles and do not force a model choice. Cursor supports repository subagent Markdown in `.cursor/agents/`. [Subagent configuration](https://cursor.com/docs/subagents).

## 3. Install the repository files

Use a pinned checkout of this library and follow [the installation guide](../docs/INSTALL.md). Open your actual application repository in Cursor, then paste [03-PROJECT-SETUP-PASTE.md](03-PROJECT-SETUP-PASTE.md) into Foreman, replacing the repository URL and selecting the actual Reviewer/Merger Bot.

The setup job runs `scripts/install.py --target /absolute/path/to/project` from the library checkout to preview changes, then runs it with `--apply` on the project's bootstrap feature branch. This copies the complete skills, references, roles, and templates; it merges the steering block and preserves project configuration. It never pushes or merges by itself.

If the Bot cannot access a checkout, provide the reviewed library URL and exact ref for its Cursor job, or perform the installation in local Cursor and push the bootstrap branch so the next Cloud job can read it. Keep every upstream skill folder intact, including its supporting scripts and references.

Do not paste only the profile and expect the remote worker to have the files. Install them in Git and push the reviewed bootstrap branch so the worker can read them. Your laptop's Downloads paths are not cloud-accessible references.

The bootstrap creates `develop` from `main` only if it is absent. It then uses `feature/BOOTSTRAP-AGENTS` for the configuration PR, independently reviews that PR, and squash-merges it into `develop`. The setup prompt explicitly authorizes that limited bootstrap work. Existing history is preserved. If existing branches diverge or `main` is missing, it reports the condition rather than resetting or renaming branches.

The setup also runs the explicitly requested `setup-matt-pocock-skills` workflow to reconcile tracker, domain, and triage documents; existing choices do not need to be asked again.

The configuration lands on `develop` first. Future cloud jobs must explicitly start from `develop`; they must not rely on the repository's default branch. Configuration reaches `main` with a later approved release.

## 4. Verify project settings and merge controls

Foreman fills `docs/agents/PROJECT.md` with the verified repository URL, tracker convention, actual check commands, Cloud environment, model choice, and Bot identities. Values marked `UNCONFIGURED` are intentionally unresolved inputs, not things to invent. An optional field can be `NOT_APPLICABLE` with a reason.

In your source-control provider, configure protections for `develop` and `main`: PRs, required checks, no force pushes, and no branch deletion. Feature PRs use squash; release PRs use merge commits. Do not enable a repository-wide squash-only policy or linear-history rule on `main` that prevents the release merge. If the provider offers only global merge-method settings, allow both methods and enforce the base-specific rule through your review process or repository automation.

The kit does not install provider-specific branch protection or CI enforcement. The setup job reports which settings are already present and gives exact manual steps for your provider when changes require your account. An AI review report is not necessarily an eligible human PR approval: keep provider-required approvals and report that gate if it cannot be satisfied.

Replace the old always-applied Foreman loader only after preserving unrelated rules. The old `.cursor/rules/grok-foreman.mdc` behavior must not force every Builder or Reviewer to become Foreman. The replacement `AGENTS.md` block routes the assigned role explicitly.

## 5. Run a small first ticket

Paste [04-FIRST-TICKET-PASTE.md](04-FIRST-TICKET-PASTE.md) into Foreman with a real ticket and requested change. This authorizes that task's feature branch, PR, and reviewed squash merge into `develop`; it does not authorize a release.

Start with one ticket at a time. After the first successful end-to-end result, increase parallel builders to two if useful. Each builder has a separate Cloud environment or checkout; Reviewer/Merger still serializes merges.

For an approved task, the flow is: brief → feature branch → implementation → independent review → squash merge to develop → post-merge checks. Foreman reports INTEGRATED when that succeeds. It reports RELEASED only after a separately approved promotion to `main`.

## 6. Prepare and approve a release

Use [05-RELEASE-PASTE.md](05-RELEASE-PASTE.md). Foreman freezes the proposed `develop` SHA, collects release review and checks, and shows the release scope. Approve the specific source and target SHAs when ready. A changed head requires a refreshed review and approval. Merging into `main` is separate from deploying; check whether your existing CI deploys automatically on a main update.

After release, synchronize `main` back into `develop` without rewriting either branch. The release procedure in the workflow covers both a fast-forward and a protected synchronization PR.

## Manual fallback when the Cursor connection is unavailable

Tell Foreman: “Prepare the complete Cursor job brief and wait for me to return its result.” Start a Cloud task in Cursor or on cursor.com/agents, select the correct repository and starting branch, and paste the brief. Return the job URL, branch, SHA, and report to Foreman. Do the same for independent review. The integration can later replace this manual relay without changing the workflow.

If a native launcher cannot honor a branch name, starting ref, or PR target, have its worker verify and establish the requested state before editing. Correct any automatically opened PR target to `develop` before review. Do not continue on an unintended branch.

## Optional shared skill

The repository includes 30 skills under `.cursor/skills/`. `SKILL-ROUTING.md` maps the crew roles to Matt's skills and documents the adapted automatic planning and architecture flows. Manual-only upstream commands retain their invocation flags. For Grok Bot, ask Foreman to save the coordination procedure as a skill named “Cursor Git Flow Crew,” retaining the current repository policy as its source of truth. Grok Bot supports skills saved from written workflows. Verify the skill appears and works on one task before adding routines. [Skills](https://docs.x.ai/grok-bot/skills-routines-and-automations).

## Practical limits

The library manifests, provenance, references, and installer behavior are validated by the repository checks; the branch sequence was tested in a temporary repository. Live Bot creation, account integration, provider permissions, and your project's checks still need the setup run. Bot descriptions and Markdown rules guide behavior; branch protections provide independent enforcement.

Grok Bot and Cursor execution have usage costs. Keep the pilot small and check your plan's usage controls. [Grok Bot billing](https://cursor.com/help/grok-bot/plans).

Product documentation checked October 9, 2026. UI labels and available integrations may vary by account.
