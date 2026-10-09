#!/usr/bin/env python3
"""Validate manifests, source provenance, routing, and local reference files."""
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def outside_fences(text):
    fence = None
    lines = []
    for line in text.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})',line)
        if match:
            marker = match[1]
            if fence is None:
                fence=marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence=None
            continue
        if fence is None:
            lines.append(line)
    return '\n'.join(lines)


def main():
    errors=[]
    lock=json.loads((ROOT/'upstream-lock.json').read_text())
    for rel, sha in lock['files'].items():
        p=ROOT/rel
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=sha:
            errors.append('Upstream hash mismatch: '+rel)
    for p in (ROOT/'plugins/matt-pocock-skills/skills').rglob('*'):
        if p.is_file() and p.relative_to(ROOT).as_posix() not in lock['files']:
            errors.append('Untracked upstream source: '+str(p.relative_to(ROOT)))
    assert len(lock['selected_paths'])==27
    if 'Copyright (c) 2026 Matt Pocock' not in (ROOT/'plugins/matt-pocock-skills/LICENSE').read_text():
        errors.append('Missing upstream copyright notice')
    marketplace=json.loads((ROOT/'.cursor-plugin/marketplace.json').read_text())
    names=set()
    for plugin in marketplace['plugins']:
        source=Path(plugin['source'])
        if source.is_absolute() or '..' in source.parts:
            errors.append('Unsafe plugin path')
            continue
        folder=ROOT/source
        manifest=json.loads((folder/'.cursor-plugin/plugin.json').read_text())
        if manifest['name']!=plugin['name'] or plugin['name'] in names:
            errors.append('Plugin identity mismatch')
        names.add(plugin['name'])
        for kind in ('skills','agents'):
            if kind in manifest:
                part=Path(manifest[kind])
                if part.is_absolute() or '..' in part.parts or not (folder/part).is_dir():
                    errors.append('Invalid component path: '+str(part))
    skills=list((ROOT/'plugins').glob('*/skills/*/SKILL.md'))
    if len(skills)!=30:
        errors.append('Expected 30 skills')
    for p in skills:
        text=p.read_text()
        if not text.startswith('---\n') or '\n---\n' not in text[4:]:
            errors.append('Missing frontmatter: '+str(p))
            continue
        meta=text.split('---\n',2)[1]
        match=re.search(r'^name: ([a-z0-9-]+)\s*$',meta,re.M)
        if not match or match[1]!=p.parent.name or not re.search(r'^description: \S',meta,re.M):
            errors.append('Invalid skill identity: '+str(p))
    for p in ROOT.rglob('*.md'):
        if '.git' in p.parts:
            continue
        for target in re.findall(r'\]\(([^)\n]+)\)',outside_fences(p.read_text())):
            if target.startswith(('http:', 'https:', '#', 'mailto:')):
                continue
            target=target.split('#',1)[0]
            if target and not (p.parent/target).exists():
                errors.append(f'Broken link in {p.relative_to(ROOT)}: {target}')
    for p in ROOT.rglob('*'):
        if '.git' in p.parts:
            continue
        if p.is_symlink():
            errors.append('Unexpected symlink: '+str(p))
    for name in ('WORKFLOW.md','SKILL-ROUTING.md'):
        if (ROOT/'templates/project/docs/agents'/name).read_bytes() != (ROOT/'plugins/cursor-crew/skills/crew-gitflow/references'/name).read_bytes():
            errors.append('Portable fallback policy drift: '+name)
    for name in ('builder','reviewer','shipper','debugger','architect','researcher','prototyper'):
        p=ROOT/f'plugins/cursor-crew/agents/grok-{name}.md'
        if 'SKILL-ROUTING.md' not in p.read_text():
            errors.append('Missing role skill routing: '+name)
    if errors:
        print('\n'.join(errors),file=sys.stderr)
        return 1
    print(f'Validated {len(skills)} skills, seven roles, plugin manifests, references, attribution, and {len(lock["files"])} upstream hashes.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
