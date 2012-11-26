import unittest, os, subprocess, shlex
import gurumate
class TestAptOps(unittest.TestCase):
    def setUp(self):
        self.package = 'python'
        self.package_version = '2.7'
        self.not_installed_package = 'testpackage.deb'
        self.final_dest_notInstalled_package = '/etc/testpackage'
        
    def test_find(self):
        self.assertTrue(gurumate.apt.find(self.package))

    def test_Not_find(self):
        self.assertFalse(gurumate.apt.find('UninstalledPackage'))
        
    def test_is_installed(self):
        self.assertTrue(gurumate.apt.is_installed(self.package))
        
    def test_get_installed_version(self):
        self.assertTrue(self.package_version in gurumate.apt.get_installed_version(self.package))
        
    def test_is_partially_installed(self):
        old_dir = os.getcwd()
        os.chdir('/var/cache/apt/archives/')
        open (self.not_installed_package, 'w+')
        self.assertTrue(gurumate.apt.is_partially_installed(self.not_installed_package + '*', self.final_dest_notInstalled_package))        
        os.remove("/var/cache/apt/archives/%s" % self.not_installed_package)
        os.chdir(old_dir)
        
    def test_is_Not_partially_installed(self):
        self.assertFalse(gurumate.apt.is_partially_installed(self.package + '*', '/etc/%s%s' % (self.package, self.package_version)))
    
    def test_is_Not_installed_by_Partially(self):
        self.assertFalse(gurumate.apt.is_partially_installed(self.not_installed_package + '*', self.final_dest_notInstalled_package))
    
    def test_in_source_list(self):
        source = subprocess.check_output(shlex.split("lsb_release -c")).strip().split(':\t')[1]
        self.assertTrue(gurumate.apt.check_in_source_list(source))
        
    def test_Not_in_source_list(self):
        self.assertFalse(gurumate.apt.check_in_source_list('wrongSource'))
