#!/usr/bin/env python3
"""Preview or install pinned project-local skills without overwriting local edits."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
LOCK = '.cursor/crew-lock.json'
BEGIN = '<!-- BEGIN GROK CURSOR CREW -->'
END = '<!-- END GROK CURSOR CREW -->'


def digest(content):
    return hashlib.sha256(content).hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.check_output(['git', *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL).strip()


def checked_path(root, rel):
    path = Path(rel)
    if path.is_absolute() or '..' in path.parts or not path.parts:
        raise ValueError('Unsafe destination: ' + rel)
    dest = root / path
    for p in [dest, *dest.parents]:
        if p == root:
            break
        if p.is_symlink():
            raise ValueError('Symlink destination is not supported: ' + str(p))
    if dest.exists() and not dest.is_file():
        raise ValueError('Destination is not a regular file: ' + str(dest))
    return dest


def payload(source):
    desired = {}
    for plugin in ('matt-pocock-skills', 'cursor-crew'):
        folder = source / 'plugins' / plugin / 'skills'
        for p in sorted(folder.rglob('*')):
            if p.is_symlink():
                raise ValueError('Source symlinks are not supported: ' + str(p))
            if p.is_file():
                desired['.cursor/skills/' + p.relative_to(folder).as_posix()] = p.read_bytes()
    agents = source / 'plugins/cursor-crew/agents'
    for p in sorted(agents.glob('*.md')):
        desired['.cursor/agents/' + p.name] = p.read_bytes()
    templates = source / 'templates/project'
    for p in sorted((templates / 'docs').rglob('*')):
        if p.is_file():
            desired[p.relative_to(templates).as_posix()] = p.read_bytes()
    for name, src in {
        'NOTICE.md':'NOTICE.md',
        'matt-pocock-LICENSE':'plugins/matt-pocock-skills/LICENSE',
        'crew-LICENSE':'LICENSE',
        'upstream-lock.json':'upstream-lock.json',
    }.items():
        desired['.cursor/crew-licenses/' + name] = (source / src).read_bytes()
    if not desired or '.cursor/skills/tdd/SKILL.md' not in desired:
        raise ValueError('Incomplete source library')
    return desired


def steering_block(text):
    if BEGIN not in text and END not in text:
        return None
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise ValueError('Ambiguous or malformed crew steering block')
    start = text.index(BEGIN)
    end = text.index(END) + len(END)
    if end < start:
        raise ValueError('Malformed crew steering block')
    return text[start:end]


def source_version(source, allow_dirty):
    try:
        top = Path(git('rev-parse', '--show-toplevel', cwd=source)).resolve()
    except subprocess.CalledProcessError:
        return {'commit':'unversioned-local', 'dirty':False}
    if top != source.resolve():
        return {'commit':'unversioned-local', 'dirty':False}
    dirty = bool(git('status', '--porcelain', '--untracked-files=all', cwd=source))
    if dirty and not allow_dirty:
        raise ValueError('Library checkout is dirty; commit it or use --allow-dirty only for development')
    return {'commit':git('rev-parse', 'HEAD', cwd=source), 'dirty':dirty}


def plan(source, target, allow_dirty=False):
    source, target = source.resolve(), target.resolve()
    if source == target or source in target.parents or target in source.parents:
        raise ValueError('Keep the library checkout separate from the target project')
    if not target.is_dir():
        raise ValueError('Target directory must exist')
    try:
        if Path(git('rev-parse', '--show-toplevel', cwd=target)).resolve() != target:
            raise ValueError('Target must be the root of its Git repository')
    except subprocess.CalledProcessError:
        raise ValueError('Target must be an initialized Git repository')
    version = source_version(source, allow_dirty)
    lock_path = checked_path(target, LOCK)
    old = json.loads(lock_path.read_text()) if lock_path.exists() else {}
    if old and old.get('schema') != 1:
        raise ValueError('Unsupported existing lock schema')
    prior = old.get('files', {})
    desired = payload(source)
    changes, conflicts, retained = {}, [], []
    # Project configuration is deliberately owned by the consumer after first use.
    project = 'docs/agents/PROJECT.md'
    project_path = checked_path(target, project)
    if project_path.exists():
        desired[project] = project_path.read_bytes()
        retained.append(project)
    for rel, content in desired.items():
        dest = checked_path(target, rel)
        current = dest.read_bytes() if dest.exists() else None
        if current == content:
            continue
        if current is not None and digest(current) != prior.get(rel):
            conflicts.append(rel)
        else:
            changes[rel] = content
    for rel, old_hash in prior.items():
        if rel in desired:
            continue
        dest = checked_path(target, rel)
        if dest.exists():
            if digest(dest.read_bytes()) != old_hash:
                conflicts.append(rel)
            else:
                changes[rel] = None

    saved_steering = old.get('steering', {})
    if saved_steering:
        rel = saved_steering['path']
    else:
        rel = 'AGENTS.md' if (target/'AGENTS.md').exists() or not (target/'CLAUDE.md').exists() else 'CLAUDE.md'
    dest = checked_path(target, rel)
    current = dest.read_text() if dest.exists() else ''
    block = steering_block((source/'templates/project/AGENTS.md').read_text())
    existing = steering_block(current)
    if existing and existing != block and digest(existing.encode()) != saved_steering.get('hash'):
        conflicts.append(rel + ' (crew block)')
    if existing:
        replacement = current.replace(existing, block)
    else:
        replacement = current + ('\n\n' if current and not current.endswith('\n') else '\n' if current else '') + block + '\n'
    if replacement != current:
        changes[rel] = replacement.encode()

    state = {
        'schema':1,
        'source_repository':'https://github.com/MalcomnM/cursor-crew-skills',
        'source':version,
        'upstream_commit':json.loads((source/'upstream-lock.json').read_text())['commit'],
        'files':{rel:digest(content) for rel,content in sorted(desired.items())},
        'steering':{'path':rel,'hash':digest(block.encode())},
        'project_owned':[project],
    }
    serialized = (json.dumps(state, indent=2) + '\n').encode()
    if not lock_path.exists() or lock_path.read_bytes() != serialized:
        changes[LOCK] = serialized
    # Validate every destination before any write, including the lock and deletions.
    for name in changes:
        checked_path(target, name)
    return changes, sorted(set(conflicts)), retained


def apply(target, changes):
    # Called only after all conflicts are checked. Each file replacement is atomic;
    # this is not a filesystem transaction. Git remains the rollback boundary.
    for rel, content in sorted(changes.items(), key=lambda item: item[0] == LOCK):
        dest = checked_path(target, rel)
        if content is None:
            dest.unlink()
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix='.crew-install-', dir=dest.parent)
        try:
            with os.fdopen(fd, 'wb') as f:
                f.write(content)
            os.replace(tmp, dest)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, required=True)
    parser.add_argument('--apply', action='store_true', help='Apply the previewed file changes')
    parser.add_argument('--allow-dirty', action='store_true', help='Development only: record a dirty source checkout')
    args = parser.parse_args()
    try:
        changes, conflicts, retained = plan(ROOT, args.target, args.allow_dirty)
        print(json.dumps({'mode':'apply' if args.apply else 'preview', 'changes':{k:'delete' if v is None else 'write' for k,v in sorted(changes.items())}, 'preserved_project_config':retained, 'conflicts':conflicts}, indent=2))
        if conflicts:
            print('No files written. Reconcile local changes before retrying.', file=sys.stderr)
            return 2
        if args.apply:
            apply(args.target.resolve(), changes)
            print('Installed. Review the Git diff; no commit or remote action was performed.')
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
