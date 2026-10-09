# Specs and tickets for crew planning

Adapted from Matt Pocock's to-spec and to-tickets at the upstream revision in upstream-lock.json. The originals and MIT notice remain in the matt-pocock-skills plugin.

## Spec

Synthesize the conversation; do not start a second interview. Include the problem from the user's perspective, intended solution, numbered user stories, settled implementation decisions, testing decisions and agreed public interfaces, exclusions, and remaining notes. Use domain vocabulary. Keep speculative implementation paths out; preserve a small prototype-derived state/type snippet only when it expresses an agreed decision better than prose.

Confirm test interfaces with the user if not already confirmed. A spec is ready when requirements, exclusions, constraints, and verification expectations are explicit. Publish to the configured tracker only within the current authority; otherwise return a draft.

## Tickets

Split the agreed spec into small vertical slices, each giving an observable result across the needed layers. Give every ticket a title, parent spec link, what to build, acceptance criteria, agreed test interfaces, and blocking tickets. Make prefactoring separately reviewable where needed. Use expand–contract for broad migrations rather than creating a permanently red intermediate develop.

Show the list with what each ticket delivers and what blocks it. Get the user's agreement on granularity and dependencies, reusing an existing explicit approval when present. Publish one issue per ticket, or one Markdown file per ticket under the configured local tracker. Create IDs first, then wire native dependency links or accurate textual references. Use configured ready-for-agent labels. Do not close the parent spec as a side effect.

## Worker brief

Pass ticket and spec pointers plus revisions, feature/[ticket], current develop SHA, accepted criteria, test seams, useful notes/prototype refs, selected skills, allowed actions, and report destination. Local tracker files must be pushed or attached where the remote Cursor job can read them; a path on Foreman's computer alone is insufficient.
