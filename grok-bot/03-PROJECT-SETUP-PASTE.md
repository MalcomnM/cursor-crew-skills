# Project setup prompt

Paste the block into Foreman. Replace the repository URL. Attach REPOSITORY-INSTALL.md or make the extracted repository/ folder available. Select the actual Reviewer/Merger Bot with @. All other project-specific values should be discovered; the Bot should ask only for information it cannot obtain.

```text
Set up this repository for my Grok Bot + Cursor crew:

Repository: REPLACE_WITH_REPOSITORY_URL
Coordinator: this Foreman Bot
Review and integration owner: the Reviewer/Merger Bot mentioned with this message
Source library: https://github.com/MalcomnM/cursor-crew-skills at a reviewed release or exact commit
Source files: that library's scripts/install.py and templates, or the supplied updated starter kit

Implement simplified Git Flow:
- main is the stable release branch.
- develop is the integration branch.
- feature/[ticket] branches start from develop; an example is feature/ABC-123.
- Squash each reviewed feature PR into develop as one ticket commit.
- Release develop to main by normal merge commit only after my explicit release approval.
- Synchronize main back to develop after release. No forced updates to shared branches.

For this setup, I authorize reading the repo and its settings; creating develop from the existing main tip only if develop is absent; installing the supplied files on feature/BOOTSTRAP-AGENTS; committing and pushing that feature branch; opening/updating its PR to develop; dispatching independent Cursor review; and squash-merging that reviewed, green setup PR into develop through Reviewer/Merger. This does not authorize a main update, deployment, history rewrite, deletion of existing work, or changing repository access/protection settings.

Inspect existing instructions, branches, skills, CI, and pending work first. If main is missing or existing branch history needs migration, report a concrete migration proposal without renaming, resetting, or overwriting branches. If develop already exists, preserve it and start from its current tip.

Install the library from a pinned checkout using scripts/install.py --target <repo> for a preview, then --apply on the bootstrap feature branch. The installer includes upstream skills with supporting files and licenses and preserves modified files/configuration. If using the updated kit instead, copy its complete repository payload.

Explicitly use /setup-matt-pocock-skills to reconcile the tracker, domain docs, triage label vocabulary, and Agent skills block. Use the existing configuration as evidence and preserve my settled choices. The setup authority includes writing those configuration files and publishing only the agreed missing tracker labels; get my choice where one is unresolved. Check that tdd, code-review, prototype references, crew-plan, crew-architecture, and crew-gitflow are discoverable.

Apply the supplied repository files. Merge the AGENTS.md crew block into the existing AGENTS.md. Reconcile conflicting filenames; preserve unrelated content. Disable only the old always-applied grok-foreman loader so Cursor workers can retain their assigned role. Preserve the old file's content in Git history. Explain any material behavior change in the setup PR.

Fill docs/agents/PROJECT.md from the actual project: repo/provider, tracker and ticket naming, Bot identities, cloud environment, install and check commands, test interfaces, merge controls, CI behavior on main, model choice, and durable task ledger. Ask me for only undiscoverable choices. Set status READY only when the required settings and access have been verified; otherwise record BLOCKED with the exact missing prerequisite.

Use the available Cursor connection. Verify it by obtaining a real job URL/ID and observing the correct repository and starting ref. If automatic dispatch is unavailable, prepare complete manual Cursor briefs and tell me where to run them. Do not install another coding product or invent a connector command.

For the bootstrap review, provide the intended workflow directly in the brief; the configuration files being reviewed cannot supply their own approval. Use the supplied reviewer instructions explicitly if the existing develop branch does not have the new role yet. Required checks must not be weakened by the bootstrap PR.

Inspect whether the provider enforces PR review, required checks, no force-push/deletion, squash feature merges, and merge-commit releases. Report exact settings I need to change manually when necessary. Never bypass an existing human approval requirement. Keep both squash and normal merge methods available when provider settings are repository-wide; main must allow release merge commits.

Once integrated, explicitly launch future Cursor workers from develop. Confirm that all supplied role and skill files can be read from that remote ref. Save the coordination procedure as a reusable Grok Bot skill if supported, pointing to the repository workflow; do not invent successful skill installation if the capability is absent.

Return: Bot identities, Cursor environment/job link, develop SHA, setup PR and squash SHA, actual required checks/results, settings still needing my action, and whether the first feature task is ready. Do not start a feature or release yet.
```
