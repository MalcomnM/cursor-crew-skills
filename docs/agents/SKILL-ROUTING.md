# Skill routing for the Cursor crew

Use Matt Pocock's actual skill bodies and their supporting files, not just a summary. Read only the skill relevant to the current phase. Find it in `.cursor/skills/<name>/SKILL.md` for project installations, or through the installed plugin's skill catalog. A Grok Bot may read the pinned library checkout when that skill is not in its menu; do not claim a native skill invocation that the product did not perform.

## Which role uses which skill

| Owner / trigger | Skills | Result |
|---|---|---|
| Foreman, new or ambiguous feature | crew-plan; grilling; domain-modeling | Agreed scope, glossary, ADRs when justified |
| Foreman, multi-session work | crew-plan's spec/ticket references, adapted from to-spec and to-tickets | Spec with agreed seams and dependency-linked vertical slices |
| User's daily planning commands | ask-matt, grill-with-docs, grill-me, to-spec, to-tickets, wayfinder | Interactive planning; invoke manual skills by name |
| First project setup | setup-matt-pocock-skills, explicitly requested in setup | Tracker, domain docs, labels, Agent skills pointers |
| Builder | tdd; codebase-design when interface shape is involved | One red/green behavior slice at agreed seams |
| Reviewer/Merger's independent review job | code-review; tdd for test quality; codebase-design for design findings | Separate Standards and Spec reports plus verification |
| Shipper or any authorized PR author | pr | Smallest useful summary, before/after evidence, merge danger |
| Debugger | diagnosing-bugs; tdd; codebase-design if the seam is inadequate | Reproduction, causal evidence, regression test |
| Architect | codebase-design; crew-architecture | Survey or alternative designs, then decisions through Foreman |
| Researcher | research | Dated, cited primary-source findings |
| Prototyper | prototype and its LOGIC.md or UI.md | Disposable runnable answer to one question |
| Foreman, incoming raw requests | triage when requested | Ready briefs; do not re-triage generated implementation tickets |
| Human-only setup | wizard | A scoped manual setup procedure, when a real human step is needed |
| After a session / explanation problem | retro; wait-what when requested | Environment improvements or a clearer explanation |
| Cross-tool transition / writing agent docs | handoff when requested; writing-for-agents | Durable context pointers and concise agent instructions |
| Personal learning / external questions | teach; to-questionnaire when requested | Optional day-to-day tools; not a required delivery stage |

## Invocation and authority

Upstream manual-only skills keep `disable-model-invocation: true` and their matching metadata. The crew does not make them auto-run merely because they are installed. Recommend them to the user, or run them when the user explicitly requests them. Reusable model-invoked primitives (tdd, grilling, domain-modeling, code-review, etc.) can be selected when relevant.

`crew-plan` and `crew-architecture` are explicitly separate adapted skills for the crew's automatic paths. They use model-invoked primitives and bundled reference procedures instead of trying to invoke manual-only upstream orchestrators. Preserve already agreed seams and decisions; do not repeat a confirmation the user has already given.

User instructions, repository policy, scoped role, and the current brief govern authority. A generic upstream workflow cannot expand a task's allowed branches, tracker writes, external communication, merge permissions, issue closure, or deployment. When it asks for an unavailable tool, use an available equivalent or report the actual missing capability.

## Required adaptations in this crew

- **implement / implement-spec:** available for your manual daily use, but the automated crew uses Builder + tdd + independent Reviewer/Merger. In an opted-in crew project, keep one `feature/[ticket]` per ticket from `develop`, squash to `develop`, and release only by the approved main policy. Replace upstream's integration-branch/reset/auto-close mechanics with WORKFLOW.md. Builder's self-review does not replace the independent gate. These manual skills never grant permission to rewrite existing work.
- **prototype / wayfinder research branches:** the crew uses `feature/[ticket]` from develop, marked prototype-only or research-only, with durable artifact links. Integrate production code only through a new scoped implementation/review. Do not create an extra prototype/*, research/*, or integration/* branch family in this project.
- **tdd:** the seams agreed with the user and recorded in the current brief satisfy the pre-agreement requirement. If absent or changed, return to Foreman; do not invent them or ask an absent user from a worker.
- **code-review:** the brief's explicit spec pointer takes precedence. Pin source/base SHAs and inspect the proposed result against the current base. Run the two axes as separate helpers when available; if readonly or nesting limits block this, the parent launches sibling helpers and aggregates their separate reports. If no helper capability exists, report a sequential two-pass fallback honestly. A skipped Spec pass or missing checks is not merge approval.
- **research:** Foreman already delegated the reading job; Researcher performs it instead of recursively spawning another Researcher. Attach the notes or commit only to its assigned feature branch with explicit authority.
- **architecture / handoff:** keep the useful report/context-pointer structure, and also persist the artifact where the next Bot or Cloud job can read it. A temporary path on one machine is not a complete handoff. Foreman owns the subsequent interactive decisions.
- **setup-matt-pocock-skills:** reconcile its issue-tracker.md, domain.md, triage-labels.md, and Agent skills block with PROJECT.md. Preserve the selected tracker and existing steering file; do not create competing configuration or duplicate AGENTS/CLAUDE content. Publishing labels requires setup scope. Empty glossary/ADR files are unnecessary.
- **to-spec / to-tickets / triage / wayfinder:** drafting and publishing are separate permissions. Preserve the required user decisions, scope confirmation, and ticket-breakdown approval. Publish or close issues only when the current request grants it. In particular, a skill's normal issue closure cannot override the crew's release/closure policy.
- **wizard:** use only for genuine human-only steps; preserve hidden input and secret handling. No generated wizard is automatically authorized to provision, migrate, or modify secrets beyond the brief.

## Installation verification

The full installation has 27 upstream skills plus crew-gitflow, crew-plan, and crew-architecture. Resolve tdd/tests.md, tdd/mocking.md, prototype/LOGIC.md, prototype/UI.md, and setup-matt-pocock-skills tracker templates before declaring the library installed. Record the library revision and upstream commit from `.cursor/crew-lock.json`. Prefer one installation source per skill name; remove duplicate plugin/project/global copies deliberately rather than assuming precedence.

Do not auto-update skills during a running ticket. Update through a separate reviewed configuration change, keep the project configuration, and rerun representative workflows before adopting the new revision.
