import unittest
import gurumate

class TestPackages(unittest.TestCase):
    def test_find_packages(self):
        self.assertEquals([], gurumate.apt.find("Balahawy"))
        results = gurumate.apt.find("redis")
        self.assertTrue(len(results) > 0)
        res = results[0]
        self.assertTrue(isinstance(res, tuple))
    
    def test_is_installed(self):
        self.assertFalse(gurumate.apt.is_installed('batata'))
        self.assertTrue(gurumate.apt.is_installed('coreutils'))
        self.assertTrue(gurumate.apt.get_installed_version('coreutils') is not None)
        self.assertTrue(gurumate.apt.get_installed_version('coreutils') != "(none)")        
