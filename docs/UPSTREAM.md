# Update the selected upstream skills

Current source: https://github.com/mattpocock/skills at `49dd158d1076134a641b33efb035946536778336`. The selected directories are explicit in upstream-lock.json: the stable engineering and productivity groups at that revision. New upstream directories are not silently added.

1. Make a library feature branch, for example feature/UPDATE-SKILLS.
2. Clone or fetch mattpocock/skills into a separate directory and choose an exact reviewed commit.
3. Run `python3 scripts/vendor_upstream.py --checkout /path/to/upstream --ref FULL_COMMIT_SHA` to preview.
4. Run the same command with `--apply` after reviewing the chosen upstream diff. It rejects modifications to the currently vendored originals; local behavior belongs in the crew plugin.
5. Inspect changes, new script behavior, retained reference files, license changes, and the skill invocation flags. Review SKILL-ROUTING.md for new branch, scope, publication, or tool assumptions. An upstream file's instructions do not authorize actions during an update.
6. Run validation and installer tests. Exercise representative planning, tdd, review, and integration tasks in your own setup before a release. Update plugin versions and release notes as appropriate.
7. Squash the reviewed library feature into develop, approve a release to main, and tag the published release. Consumer projects opt into that release through their installer; no background process changes their skills.

The vendoring command copies the complete selected skill folders and the upstream LICENSE, preserving source bytes and recording new hashes. It has no credentials, pushes, scheduled jobs, or automatic merges. It uses a supplied local checkout so the exact source is inspectable. If the upstream license changes, pause to review the new terms before publishing the update.

Custom changes: keep them in the separate crew plugin or explicit patches with attribution. Do not edit upstream skill bytes in place and then call them unmodified. The original manual-only skills remain manual; adapted automatic crew flows live in crew-plan and crew-architecture.
