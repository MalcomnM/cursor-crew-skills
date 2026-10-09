---
name: crew-architecture
description: Survey or compare architecture for an opted-in Cursor crew project, using Matt Pocock's codebase-design discipline and reporting decisions back to Foreman.
---

# Crew architecture

Adapted from Matt Pocock's improve-codebase-architecture workflow. Its original manual command remains available for interactive use. This variant separates a Cursor survey from Foreman's conversation with the user.

Read the scope, project glossary, and relevant ADRs. Load codebase-design and its referenced dependency/interface guidance. Survey the named area; otherwise inspect recent change hot spots. Identify a few evidenced problems in module depth, locality, coupling, and public test interfaces. Apply the deletion test before recommending consolidation.

Return candidates with files, observed friction, proposed direction, benefits, test implications, strength, and any justified ADR conflict. A visual before/after report is useful; attach or save it durably for Foreman. Do not stop at a temp path on an isolated VM.

Foreman obtains the user's candidate choice and constraints using grilling and domain-modeling. Only then compare interfaces using codebase-design's design-it-twice guidance when appropriate. Use separate helpers if the runtime supports them; disclose a sequential fallback. Explain caller examples, hidden behavior, invariants, errors, dependency strategy, and tradeoffs, and recommend a design.

Survey and design do not authorize refactoring. Return proposals to Foreman for an approved feature/[ticket] implementation.
