#!/usr/bin/env python3
"""Copy setup-crew roles and docs, and merge the AGENTS.md crew block.

Uses only the Python standard library. Role files that differ from the bundled
copy are left in place and reported as conflicts. Existing docs/agents files
are left in place. Text outside the crew markers in AGENTS.md is preserved.
"""
import argparse
import json
import os
from pathlib import Path
import sys
import tempfile

BEGIN = '<!-- BEGIN GROK CURSOR CREW -->'
END = '<!-- END GROK CURSOR CREW -->'
SKILL_ROOT = Path(__file__).resolve().parents[1]


def crew_span(text):
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise ValueError('Malformed crew block in skill assets')
    start = text.index(BEGIN)
    end = text.index(END) + len(END)
    if end < start:
        raise ValueError('Malformed crew block in skill assets')
    return text[start:end]


def checked_path(root, rel):
    path = Path(rel)
    if path.is_absolute() or '..' in path.parts or not path.parts:
        raise ValueError('Unsafe destination: ' + rel)
    dest = root / path
    for parent in [dest, *dest.parents]:
        if parent == root:
            break
        if parent.is_symlink():
            raise ValueError('Symlink destination is not supported: ' + str(parent))
    if dest.exists() and not dest.is_file():
        raise ValueError('Destination is not a regular file: ' + str(dest))
    return dest


def merged_agents(current, span):
    body = span if span.endswith('\n') else span + '\n'
    if BEGIN not in current and END not in current:
        if not current:
            return body
        separator = '\n' if current.endswith('\n') else '\n\n'
        return current + separator + body
    if current.count(BEGIN) != 1 or current.count(END) != 1:
        raise ValueError('Ambiguous or malformed crew steering block')
    start = current.index(BEGIN)
    end = current.index(END) + len(END)
    if end < start:
        raise ValueError('Malformed crew steering block')
    return current[:start] + span + current[end:]


def plan(target, assets=None):
    target = Path(target).resolve()
    assets = (Path(assets) if assets else SKILL_ROOT / 'assets').resolve()
    if not target.is_dir():
        raise ValueError('Target directory must exist')
    agents = sorted((assets / 'agents').glob('grok-*.md'))
    doc_root = assets / 'project' / 'docs'
    docs = [p for p in sorted(doc_root.rglob('*')) if p.is_file()]
    block_path = assets / 'project' / 'AGENTS.md'
    if len(agents) != 7 or not block_path.is_file() or len(docs) != 3:
        raise ValueError('Incomplete setup-crew assets')
    for src in [*agents, block_path, *docs]:
        if src.is_symlink():
            raise ValueError('Source symlinks are not supported: ' + str(src))
    span = crew_span(block_path.read_text())
    changes, conflicts, skipped = {}, [], []
    for src in agents:
        rel = '.cursor/agents/' + src.name
        dest = checked_path(target, rel)
        content = src.read_bytes()
        if dest.exists():
            if dest.read_bytes() != content:
                conflicts.append(rel)
            continue
        changes[rel] = content
    for src in docs:
        rel = src.relative_to(assets / 'project').as_posix()
        dest = checked_path(target, rel)
        content = src.read_bytes()
        if dest.exists():
            if dest.read_bytes() != content:
                skipped.append(rel)
            continue
        changes[rel] = content
    dest = checked_path(target, 'AGENTS.md')
    current = dest.read_text() if dest.exists() else ''
    try:
        replacement = merged_agents(current, span)
    except ValueError:
        conflicts.append('AGENTS.md (crew block)')
    else:
        encoded = replacement.encode()
        if not dest.exists() or dest.read_bytes() != encoded:
            changes['AGENTS.md'] = encoded
    for rel in changes:
        checked_path(target, rel)
    return changes, sorted(set(conflicts)), sorted(set(skipped))


def apply(target, changes):
    target = Path(target).resolve()
    for rel, content in sorted(changes.items()):
        dest = checked_path(target, rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix='.setup-crew-', dir=dest.parent)
        try:
            with os.fdopen(fd, 'wb') as handle:
                handle.write(content)
            os.replace(tmp, dest)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, required=True)
    parser.add_argument('--assets', type=Path, help='Override the bundled assets directory')
    parser.add_argument('--dry-run', action='store_true', help='Print the plan and write nothing')
    args = parser.parse_args()
    try:
        changes, conflicts, skipped = plan(args.target, args.assets)
        print(json.dumps({
            'mode': 'dry-run' if args.dry_run else 'apply',
            'changes': {rel: 'write' for rel in sorted(changes)},
            'conflicts': conflicts,
            'skipped': skipped,
        }, indent=2))
        if not args.dry_run:
            apply(args.target.resolve(), changes)
        if conflicts:
            print('Left locally changed role files in place.', file=sys.stderr)
            return 2
        return 0
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
