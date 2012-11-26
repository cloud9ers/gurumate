import unittest, os, subprocess, shlex
import gurumate
class TestApacheOps(unittest.TestCase):
    def setUp(self):
        self.module = 'actions'
        self.mimetype = 'x-python'
        subprocess.check_output(shlex.split("sudo a2enmod %s" % self.module))
        subprocess.check_output(shlex.split("sudo /etc/init.d/apache2 restart"))
        subprocess.check_output(shlex.split("sudo /etc/init.d/apache2 reload"))
        
    def tearDown(self):
        subprocess.check_output(shlex.split("sudo a2dismod %s" % self.module))
        subprocess.check_output(shlex.split("sudo /etc/init.d/apache2 stop"))
        
    def test_is_module_enabled(self):
        self.assertTrue(gurumate.apache.is_module_enabled(self.module))

    def test_isNot_module_enabled(self):
        self.assertFalse(gurumate.apache.is_module_enabled('wrongmodule'))
    
    def test_is_recently_restarted(self):
        self.assertTrue(gurumate.apache.is_recently_restarted())
    
    def test_is_recently_reloaded(self):
        self.assertTrue(gurumate.apache.is_recently_reloaded())
        
    def test_is_mime_type_enabled(self):
        self.assertTrue(gurumate.apache.is_mime_type_enabled(self.mimetype))

    def test_isNot_mime_type_enabled(self):
        self.assertFalse(gurumate.apache.is_mime_type_enabled('Wrong-mimetype'))
        
    def test_check_apache_running_php(self):
        self.assertTrue(gurumate.apache.check_apache_running_php())
