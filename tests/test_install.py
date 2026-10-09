import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('installer',ROOT/'scripts/install.py')
installer=importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name)
        self.source=self.base/'library'
        shutil.copytree(ROOT,self.source,ignore=shutil.ignore_patterns('.git','__pycache__'))
        self.target=self.base/'project'
        self.target.mkdir()
        subprocess.run(['git','init','-q',str(self.target)],check=True)

    def install(self):
        changes,conflicts,_=installer.plan(self.source,self.target)
        self.assertEqual(conflicts,[])
        installer.apply(self.target,changes)
        return changes

    def test_preview_has_no_writes_and_install_is_idempotent(self):
        changes,conflicts,_=installer.plan(self.source,self.target)
        self.assertFalse(conflicts)
        self.assertTrue(changes)
        self.assertFalse((self.target/'.cursor').exists())
        self.install()
        self.assertEqual(self.install(),{})
        self.assertEqual(len(list((self.target/'.cursor/skills').glob('*/SKILL.md'))),30)
        self.assertTrue((self.target/'.cursor/skills/tdd/tests.md').is_file())
        self.assertTrue((self.target/'.cursor/skills/prototype/UI.md').is_file())
        self.assertTrue((self.target/'.cursor/crew-licenses/matt-pocock-LICENSE').is_file())

    def test_unmanaged_conflict_prevents_every_write(self):
        p=self.target/'.cursor/skills/tdd/SKILL.md'
        p.parent.mkdir(parents=True)
        p.write_text('My own TDD skill')
        result=subprocess.run(['python3',str(self.source/'scripts/install.py'),'--target',str(self.target),'--apply'],capture_output=True,text=True)
        self.assertEqual(result.returncode,2,result.stderr)
        self.assertEqual(p.read_text(),'My own TDD skill')
        self.assertFalse((self.target/'docs').exists())
        self.assertFalse((self.target/installer.LOCK).exists())

    def test_local_skill_edit_blocks_update(self):
        self.install()
        p=self.target/'.cursor/skills/tdd/SKILL.md'
        p.write_text(p.read_text()+'\nMy customization\n')
        _,conflicts,_=installer.plan(self.source,self.target)
        self.assertIn('.cursor/skills/tdd/SKILL.md',conflicts)

    def test_project_configuration_and_other_steering_are_preserved(self):
        (self.target/'CLAUDE.md').write_text('# Existing rules\nKeep this.\n')
        self.install()
        self.assertFalse((self.target/'AGENTS.md').exists())
        self.assertTrue((self.target/'CLAUDE.md').read_text().startswith('# Existing rules\nKeep this.\n'))
        p=self.target/'docs/agents/PROJECT.md'
        p.write_text('# My configured project\nStatus: READY\n')
        self.install()
        self.assertEqual(p.read_text(),'# My configured project\nStatus: READY\n')
        self.assertEqual((self.target/'CLAUDE.md').read_text().count(installer.BEGIN),1)

    def test_clean_managed_update_and_removal(self):
        self.install()
        source=self.source/'plugins/matt-pocock-skills/skills/tdd/tests.md'
        source.write_text(source.read_text()+'\nAn updated reference\n')
        removed=self.source/'plugins/matt-pocock-skills/skills/tdd/mocking.md'
        removed.unlink()
        changes=self.install()
        self.assertIn('.cursor/skills/tdd/tests.md',changes)
        self.assertIsNone(changes['.cursor/skills/tdd/mocking.md'])
        self.assertFalse((self.target/'.cursor/skills/tdd/mocking.md').exists())

    def test_modified_removed_file_is_retained_as_conflict(self):
        self.install()
        source=self.source/'plugins/matt-pocock-skills/skills/tdd/mocking.md'
        target=self.target/'.cursor/skills/tdd/mocking.md'
        target.write_text('My local changes')
        source.unlink()
        _,conflicts,_=installer.plan(self.source,self.target)
        self.assertIn('.cursor/skills/tdd/mocking.md',conflicts)
        self.assertEqual(target.read_text(),'My local changes')

    def test_symlink_destination_rejected(self):
        external=self.base/'elsewhere'
        external.mkdir()
        (self.target/'.cursor').symlink_to(external,target_is_directory=True)
        with self.assertRaises(ValueError):
            installer.plan(self.source,self.target)
        self.assertEqual(list(external.iterdir()),[])

    def test_modified_crew_block_is_not_overwritten(self):
        self.install()
        target=self.target/'AGENTS.md'
        target.write_text(target.read_text().replace('Cursor crew','My custom crew'))
        _,conflicts,_=installer.plan(self.source,self.target)
        self.assertIn('AGENTS.md (crew block)',conflicts)

    def test_source_sha_is_recorded_and_dirty_source_rejected(self):
        subprocess.run(['git','init','-q',str(self.source)],check=True)
        subprocess.run(['git','-C',str(self.source),'add','.'],check=True)
        subprocess.run(['git','-C',str(self.source),'-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','Initial library'],check=True)
        self.install()
        lock=json.loads((self.target/installer.LOCK).read_text())
        sha=subprocess.check_output(['git','-C',str(self.source),'rev-parse','HEAD'],text=True).strip()
        self.assertEqual(lock['source']['commit'],sha)
        (self.source/'README.md').write_text('Changed')
        with self.assertRaises(ValueError):
            installer.plan(self.source,self.target)


if __name__=='__main__':
    unittest.main()
