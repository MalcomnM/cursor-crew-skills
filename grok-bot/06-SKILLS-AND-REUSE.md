# Skills and reuse

The reusable library is https://github.com/MalcomnM/cursor-crew-skills. Use the README and docs/INSTALL.md there to install a pinned revision into each new project. The project installer is the recommended route for cloud execution because the complete skills, references, roles, and policy are committed with the project.

For interactive Cursor use, import the repository in Customize using From GitHub Repository, then install both matt-pocock-skills and cursor-crew. This adds the skill library; project setup is still needed. Avoid duplicate installations of the same skill names. Project-local installations already include both libraries and do not also need the plugins.

In Grok Bot, update Foreman with 01-FOREMAN-PASTE.md and Reviewer/Merger with 02-REVIEWER-MERGER-PASTE.md. Use 03-PROJECT-SETUP-PASTE.md for a project. Give Foreman an accessible pinned library checkout or the required skill files with their references. A skill installed only on your local Cursor does not establish that Grok Bot or a Cloud Agent can access it. Verify access in each environment.

Foreman uses crew-plan with Matt's grilling and domain-modeling primitives. Builder uses tdd; Reviewer uses code-review; Shipper uses pr; Debugger uses diagnosing-bugs; Architect uses crew-architecture and codebase-design; Researcher uses research; Prototyper uses prototype. Supporting files are part of the installation, not optional snippets.

Your familiar manual commands remain installed: ask-matt, setup-matt-pocock-skills, grill-with-docs, grill-me, to-spec, to-tickets, implement, implement-spec, improve-codebase-architecture, triage, wayfinder, retro, handoff, wait-what, to-questionnaire, and teach. Their manual-only flags are preserved. The crew uses its adapted orchestrators for automation, with the differences documented in SKILL-ROUTING.md.

Once configured, tell Foreman: “Use the crew for this ticket. Apply the skills in SKILL-ROUTING.md and report the library revision and skills used.” This does not authorize new branches, releases, or tracker changes beyond your task's existing scope.

Updates are deliberate: update the library from an exact upstream commit, review and test it, then install a reviewed library revision into each consumer project on a configuration feature branch. Do not run git pull inside .cursor/skills or let a background task rewrite skill files during an active ticket.
