import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/crew/setup-crew'
SCRIPT = SKILL / 'scripts/copy_assets.py'
spec = importlib.util.spec_from_file_location('setup_crew', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

ROLES = (
    'grok-architect.md',
    'grok-builder.md',
    'grok-debugger.md',
    'grok-prototyper.md',
    'grok-researcher.md',
    'grok-reviewer.md',
    'grok-shipper.md',
)


class SetupCrewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.target = Path(self.tmp.name) / 'project'
        self.target.mkdir()

    def apply(self):
        changes, conflicts, skipped = helper.plan(self.target)
        self.assertEqual(conflicts, [])
        self.assertEqual(skipped, [])
        helper.apply(self.target, changes)
        return changes

    def test_fresh_project_receives_roles_crew_block_and_docs(self):
        dry = subprocess.run(
            ['python3', str(SCRIPT), '--target', str(self.target), '--dry-run'],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(dry.returncode, 0, dry.stderr)
        self.assertEqual(json.loads(dry.stdout)['mode'], 'dry-run')
        self.assertFalse((self.target / '.cursor').exists())
        self.assertFalse((self.target / 'AGENTS.md').exists())

        self.apply()
        block = (SKILL / 'assets/project/AGENTS.md').read_bytes()
        self.assertEqual((self.target / 'AGENTS.md').read_bytes(), block)
        self.assertEqual((self.target / 'AGENTS.md').read_text().count(helper.BEGIN), 1)
        for name in ROLES:
            dest = self.target / '.cursor/agents' / name
            self.assertEqual(dest.read_bytes(), (SKILL / 'assets/agents' / name).read_bytes())
        for name in ('PROJECT.md', 'WORKFLOW.md', 'SKILL-ROUTING.md'):
            dest = self.target / 'docs/agents' / name
            self.assertEqual(dest.read_bytes(), (SKILL / 'assets/project/docs/agents' / name).read_bytes())

    def test_existing_agents_md_keeps_text_outside_the_crew_block(self):
        original = '# Flight manual\n\nKeep this sentence.\n'
        (self.target / 'AGENTS.md').write_text(original)
        self.apply()
        text = (self.target / 'AGENTS.md').read_text()
        self.assertTrue(text.startswith(original))
        self.assertEqual(text.count(helper.BEGIN), 1)
        self.assertEqual(text.count(helper.END), 1)
        start = text.index(helper.BEGIN)
        end = text.index(helper.END) + len(helper.END)
        canonical = (SKILL / 'assets/project/AGENTS.md').read_text()
        canonical = canonical[canonical.index(helper.BEGIN):canonical.index(helper.END) + len(helper.END)]
        self.assertEqual(text[start:end], canonical)
        self.assertEqual(text[:start], original + '\n')

        surrounded = '# Before\n' + canonical.replace('Grok Bot and Cursor crew', 'Edited crew title') + '\n# After\n'
        (self.target / 'AGENTS.md').write_text(surrounded)
        changes, conflicts, skipped = helper.plan(self.target)
        self.assertEqual(conflicts, [])
        self.assertEqual(skipped, [])
        helper.apply(self.target, changes)
        merged = (self.target / 'AGENTS.md').read_text()
        self.assertTrue(merged.startswith('# Before\n'))
        self.assertTrue(merged.endswith('\n# After\n'))
        self.assertIn('Grok Bot and Cursor crew', merged)
        self.assertNotIn('Edited crew title', merged)
        self.assertEqual(merged.count(helper.BEGIN), 1)

    def test_locally_modified_role_file_is_reported_and_left_in_place(self):
        custom = 'Local builder role. Do not replace.\n'
        role = self.target / '.cursor/agents/grok-builder.md'
        role.parent.mkdir(parents=True)
        role.write_text(custom)
        changes, conflicts, skipped = helper.plan(self.target)
        self.assertIn('.cursor/agents/grok-builder.md', conflicts)
        self.assertNotIn('.cursor/agents/grok-builder.md', changes)
        self.assertEqual(skipped, [])
        helper.apply(self.target, changes)
        self.assertEqual(role.read_text(), custom)
        self.assertEqual(
            (self.target / '.cursor/agents/grok-shipper.md').read_bytes(),
            (SKILL / 'assets/agents/grok-shipper.md').read_bytes(),
        )

    def test_rerun_is_idempotent(self):
        first = self.apply()
        self.assertTrue(first)
        snapshot = {
            path.relative_to(self.target).as_posix(): path.read_bytes()
            for path in self.target.rglob('*') if path.is_file()
        }
        changes, conflicts, skipped = helper.plan(self.target)
        self.assertEqual(changes, {})
        self.assertEqual(conflicts, [])
        self.assertEqual(skipped, [])
        helper.apply(self.target, changes)
        again = {
            path.relative_to(self.target).as_posix(): path.read_bytes()
            for path in self.target.rglob('*') if path.is_file()
        }
        self.assertEqual(again, snapshot)

    def test_existing_docs_are_not_clobbered(self):
        project = self.target / 'docs/agents/PROJECT.md'
        project.parent.mkdir(parents=True)
        project.write_text('# Mine\nStatus: READY\n')
        changes, conflicts, skipped = helper.plan(self.target)
        self.assertEqual(conflicts, [])
        self.assertIn('docs/agents/PROJECT.md', skipped)
        self.assertNotIn('docs/agents/PROJECT.md', changes)
        helper.apply(self.target, changes)
        self.assertEqual(project.read_text(), '# Mine\nStatus: READY\n')
        self.assertTrue((self.target / 'docs/agents/WORKFLOW.md').is_file())


if __name__ == '__main__':
    unittest.main()
