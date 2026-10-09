---
name: crew-plan
description: Plan an approved Cursor crew task with the user using Matt Pocock's grilling and domain-modeling primitives, then prepare a spec and dependency-linked tickets for Cursor workers.
---

# Crew planning

This is the crew's adapted planning procedure, derived from Matt Pocock's grill-with-docs, to-spec, and to-tickets workflows. The original manual commands remain separately installed. Use this skill only when coordinating work for an opted-in crew project.

Read PROJECT.md and SKILL-ROUTING.md in the target project's docs/agents/. Read the current request, existing spec, glossary, ADRs, and previous decisions. Determine whether the ticket is already ready; do not interview the user again about settled decisions.

For unresolved product decisions, load the model-invoked grilling and domain-modeling skills. Foreman conducts the conversation. Facts come from source inspection or a scoped research job; the user settles behavior and tradeoffs. Use the configured document locations to preserve agreed terms and justified ADRs within the current write authority.

For a small, complete ticket, record accepted outcomes and user-agreed test seams, then prepare the Builder brief. For multi-session work, use [spec and ticket reference](references/spec-and-tickets.md). Confirm test seams and the proposed ticket breakdown before publishing. When planning is authorized but tracker writes are not, return drafts for the user to approve.

Each ticket must be verifiable and carry its dependency edges. A prerequisite is satisfied after its approved squash commit reaches develop, not merely after a worker says DONE. For a wide mechanical refactor, use expand–contract batches that can stay green. If no green split is possible, propose a larger atomic ticket or a separately approved workflow; do not invent a red integration branch.

Dispatch through Foreman only after the requested scope is settled. Pass pointers to the exact spec/ticket, feature branch, base SHA, agreed seams, applicable skills, authority, and return destination. Close planning with the agreed decision record, drafts or published links, and the next owner.
