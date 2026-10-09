# Install in projects and keep updates reviewable

Use a reviewed tag or exact commit of https://github.com/MalcomnM/cursor-crew-skills. Keep the checkout outside the target application repo. Python 3.9+ and Git are required; the installer uses only Python's standard library and does not download or execute upstream scripts.

## New project

Create an ordinary Git repository and its initial commit first. On a configuration feature branch, run the preview and apply commands from README.md. If develop does not yet exist, the Grok Bot setup prompt explains the limited bootstrap that creates it from main. The installer itself changes files only; it never creates or switches branches.

The complete installation includes skills and supporting files in .cursor/skills, roles in .cursor/agents, policy and a configuration template in docs/agents, license notices, and .cursor/crew-lock.json. A marked crew block is merged into AGENTS.md, or CLAUDE.md when that is the existing steering file. Text outside that block is preserved. PROJECT.md is initialized once and then left under project ownership.

Run the explicitly requested setup-matt-pocock-skills procedure from the setup prompt. Reconcile its issue-tracker.md, domain.md, and triage-labels.md with PROJECT.md and the current steering file. Pick the tracker you actually use and preserve existing labels. Install access alone does not authorize posting or closing issues.

Review and commit the files. Start cloud jobs from develop after the configuration PR is integrated. The worker should resolve the installed skill and its references, report the library revision, and run a small representative task before broad rollout.

## Update a project

Update the separate library checkout to a reviewed release or full commit. Run the same preview and apply commands from that checkout against the application repo on a new configuration branch. Read the diff and .cursor/crew-lock.json before integrating.

Existing files are updated only when they still match the previous installed hashes. Files with local edits cause a conflict and no files are written. PROJECT.md is retained deliberately. If the new library removes a managed file, the installer deletes it only if it still matches the previous hash. There is no force-overwrite option. Resolve differences by saving your customization in a reviewed library change, or manually reconciling and committing the target, then rerun.

The lock records source repository, exact checkout commit (or an explicit unversioned-local marker when run from an unpacked archive), upstream revision, installed content hashes, and the steering block hash. A dirty library checkout is rejected unless --allow-dirty is explicitly supplied for development; that override records the dirty state. It is not the release path.

## Existing starter kit

The first generation had no lock file. If those files differ, the installer will report conflicts rather than overwrite them. Back up or commit your current project, compare the new templates with your installed files, retain PROJECT.md and local configuration, and make the migration as a reviewed feature change. Files identical to the library can be adopted automatically.

## Plugins instead of project copies

Import the public repo in Cursor Customize and install its two plugins. This is convenient for daily interactive use. Do not also leave duplicate global or project copies of the same skill unless you deliberately manage their precedence. The manifests use only documented paths and no credentials or connectors.

For Grok Bot, install supported plugin capabilities where your account exposes them, or give the Bot a pinned clone of the public library and tell it where to read the required SKILL.md and references. Grok Bot's private skill/menu state and Cursor's desktop/project state are distinct. Verify access rather than assuming sync. The repository does not claim that pasting Markdown alone creates a native plugin or installs the Cursor connection.

## Removal

There is no automatic uninstall. Use the lock file to identify managed paths, inspect your Git diff, and remove only the selected library content in a reviewed project change. Preserve project-owned configuration and your other skills.
