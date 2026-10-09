#!/usr/bin/env python3
"""Preview or refresh selected upstream folders from an exact local Git commit."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile
import io
from install import checked_path

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--checkout', type=Path, required=True)
    p.add_argument('--ref', required=True, help='Full 40-character reviewed upstream SHA')
    p.add_argument('--apply', action='store_true')
    args = p.parse_args()
    if not re.fullmatch(r'[0-9a-f]{40}', args.ref):
        p.error('--ref must be a full lowercase commit SHA')
    lock = json.loads((ROOT/'upstream-lock.json').read_text())
    old = lock['files']
    conflicts = [name for name, sha in old.items() if not (ROOT/name).is_file() or digest((ROOT/name).read_bytes()) != sha]
    if conflicts:
        print('Vendored originals were modified; preserve customizations outside upstream source:\n'+'\n'.join(conflicts), file=sys.stderr)
        return 2
    resolved = subprocess.check_output(['git','-C',str(args.checkout),'rev-parse',args.ref+'^{commit}'],text=True).strip()
    if resolved != args.ref:
        raise ValueError('Commit identity mismatch')
    paths = lock['selected_paths']
    raw = subprocess.check_output(['git','-C',str(args.checkout),'archive',args.ref,'LICENSE',*paths])
    desired = {}
    with tarfile.open(fileobj=io.BytesIO(raw),mode='r:') as archive:
        for member in archive.getmembers():
            if member.isdir():
                continue
            if not member.isfile() or '..' in Path(member.name).parts or Path(member.name).is_absolute():
                raise ValueError('Unexpected archive entry: '+member.name)
            if member.name == 'LICENSE':
                dest = 'plugins/matt-pocock-skills/LICENSE'
            else:
                owners = [base for base in paths if member.name.startswith(base+'/')]
                if len(owners) != 1:
                    raise ValueError('Unknown upstream path: '+member.name)
                base = owners[0]
                dest = 'plugins/matt-pocock-skills/skills/'+Path(base).name+'/'+member.name[len(base)+1:]
            desired[dest] = archive.extractfile(member).read()
    if 'plugins/matt-pocock-skills/LICENSE' not in desired:
        raise ValueError('Upstream license is missing')
    for selected in paths:
        if 'plugins/matt-pocock-skills/skills/'+Path(selected).name+'/SKILL.md' not in desired:
            raise ValueError('Selected skill missing: '+selected)
    license_path = 'plugins/matt-pocock-skills/LICENSE'
    if desired[license_path] != (ROOT/license_path).read_bytes():
        print('Upstream LICENSE changed. Review the terms and adapt the vendoring policy explicitly before applying.', file=sys.stderr)
        return 2
    changes = [name for name, content in desired.items() if digest(content) != old.get(name)]
    removed = sorted(set(old)-set(desired))
    new_collisions = [name for name in changes if name not in old and (ROOT/name).exists() and (ROOT/name).read_bytes() != desired[name]]
    if new_collisions:
        raise ValueError('New upstream files collide with local content: '+', '.join(new_collisions))
    print(json.dumps({'from':lock['commit'],'to':args.ref,'changed':changes,'removed':removed,'mode':'apply' if args.apply else 'preview'},indent=2))
    if not args.apply:
        return 0
    for name in set(old) | set(desired):
        checked_path(ROOT, name)
    for name in removed:
        (ROOT/name).unlink()
    for name,content in desired.items():
        dest=ROOT/name
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(content)
    previous=lock['commit']
    lock['commit']=args.ref
    lock['files']={name:digest(content) for name,content in sorted(desired.items())}
    (ROOT/'upstream-lock.json').write_text(json.dumps(lock,indent=2)+'\n')
    for name in ('README.md','NOTICE.md','docs/UPSTREAM.md'):
        dest=checked_path(ROOT,name)
        text=dest.read_text()
        dest.write_text(text.replace(previous,args.ref).replace(previous[:12],args.ref[:12]))
    print('Updated vendored source and lock. Review routing and documentation before committing.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(str(exc),file=sys.stderr)
        raise SystemExit(1)
