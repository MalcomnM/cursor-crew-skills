import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]


class VendorTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name)
        self.library=self.base/'library'
        shutil.copytree(ROOT,self.library,ignore=shutil.ignore_patterns('.git','__pycache__'))
        self.upstream=self.base/'upstream'
        self.upstream.mkdir()
        self.lock=json.loads((self.library/'upstream-lock.json').read_text())
        for entry in self.lock['selected_paths']:
            shutil.copytree(self.library/'plugins/matt-pocock-skills/skills'/Path(entry).name,self.upstream/entry)
        shutil.copyfile(self.library/'plugins/matt-pocock-skills/LICENSE',self.upstream/'LICENSE')
        self.git('init','-q')
        self.git('config','user.name','Test')
        self.git('config','user.email','test@example.invalid')
        self.commit('Initial source')

    def git(self,*args):
        return subprocess.check_output(['git',*args],cwd=self.upstream,text=True).strip()

    def commit(self,message):
        self.git('add','.')
        self.git('commit','-qm',message)
        return self.git('rev-parse','HEAD')

    def run_vendor(self,ref,apply=False):
        args=['python3',str(self.library/'scripts/vendor_upstream.py'),'--checkout',str(self.upstream),'--ref',ref]
        if apply:
            args.append('--apply')
        return subprocess.run(args,capture_output=True,text=True)

    def test_preview_then_apply_updates_source_hashes_and_attribution(self):
        path=self.upstream/'skills/engineering/tdd/tests.md'
        path.write_text(path.read_text()+'\nReviewed upstream update\n')
        ref=self.commit('Update test reference')
        original=(self.library/'upstream-lock.json').read_bytes()
        r=self.run_vendor(ref)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual((self.library/'upstream-lock.json').read_bytes(),original)
        r=self.run_vendor(ref,True)
        self.assertEqual(r.returncode,0,r.stderr)
        new=json.loads((self.library/'upstream-lock.json').read_text())
        self.assertEqual(new['commit'],ref)
        target=self.library/'plugins/matt-pocock-skills/skills/tdd/tests.md'
        self.assertEqual(target.read_bytes(),path.read_bytes())
        self.assertEqual(new['files'][target.relative_to(self.library).as_posix()],hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertIn(ref,(self.library/'NOTICE.md').read_text())

    def test_license_change_blocks_apply(self):
        (self.upstream/'LICENSE').write_text('Different license')
        ref=self.commit('Change terms')
        original=(self.library/'upstream-lock.json').read_bytes()
        r=self.run_vendor(ref,True)
        self.assertEqual(r.returncode,2,r.stderr)
        self.assertEqual((self.library/'upstream-lock.json').read_bytes(),original)

    def test_local_vendor_edit_blocks_apply(self):
        target=self.library/'plugins/matt-pocock-skills/skills/tdd/tests.md'
        target.write_text('Local customization')
        r=self.run_vendor(self.git('rev-parse','HEAD'),True)
        self.assertEqual(r.returncode,2,r.stderr)
        self.assertEqual(target.read_text(),'Local customization')


if __name__=='__main__':
    unittest.main()
