import unittest
from impl.common.dir_struct import createScriptRepresentationFrom, all_patch_scripts_sorted_asc, all_rollback_scripts_sorted_desc

class DirectoryStructureTest(unittest.TestCase):
    def test_script_representation(self):
        script = createScriptRepresentationFrom('tests/impl/patches/1', 'patch', 'test-a.sql')
        self.assertEqual('tests/impl/patches/1/patch', script.getPath())
        self.assertEqual('test-a.sql', script.getName())
        self.assertEqual(1, script.getPatchNumber())
        self.assertEqual(3367243489, script.getChecksum())
        return


    def test_patch_scripts_natural_order(self):
        scripts = all_patch_scripts_sorted_asc('tests/impl')

        self.assertEqual('tests/impl/patches/1/patch', scripts[0].getPath())
        self.assertEqual('test-a.sql', scripts[0].getName())

        self.assertEqual('tests/impl/patches/1/patch', scripts[1].getPath())
        self.assertEqual('test-b.sql', scripts[1].getName())

        self.assertEqual('tests/impl/patches/2/patch', scripts[2].getPath())
        self.assertEqual('test-c.sql', scripts[2].getName())

        self.assertEqual('tests/impl/patches/2/patch', scripts[3].getPath())
        self.assertEqual('test-d.sql', scripts[3].getName())

        return


    def test_rollback_scripts_reverse_order(self):
        scripts = all_rollback_scripts_sorted_desc('tests/impl')

        self.assertEqual('tests/impl/patches/2/rollback', scripts[0].getPath())
        self.assertEqual('test-d.sql', scripts[0].getName())

        self.assertEqual('tests/impl/patches/2/rollback', scripts[1].getPath())
        self.assertEqual('test-c.sql', scripts[1].getName())

        self.assertEqual('tests/impl/patches/1/rollback', scripts[2].getPath())
        self.assertEqual('test-b.sql', scripts[2].getName())

        self.assertEqual('tests/impl/patches/1/rollback', scripts[3].getPath())
        self.assertEqual('test-a.sql', scripts[3].getName())

        return


if __name__ == '__main__':
    unittest.main()
