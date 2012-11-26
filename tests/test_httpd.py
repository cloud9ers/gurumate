import unittest, os, psutil, subprocess, shlex
import gurumate
from gurumate.base import ValidationError
class TestHttpdOps(unittest.TestCase):
    
    def setUp(self):
        self.proc = 'apache2'
        self.port = int(os.popen("sudo cat /etc/apache2/ports.conf | grep Listen | cut -d ' ' -f2").readline().strip())
        subprocess.check_output(shlex.split('sudo service apache2 start'))

    def tearDown(self):
        subprocess.check_output(shlex.split('sudo service apache2 stop'))
    
    def test_check_running(self):
        self.assertTrue(gurumate.httpd.check_running(self.proc))
        
    def test_check_isNot_running(self):
        subprocess.check_output(shlex.split('sudo service apache2 stop'))
        self.assertRaises(ValidationError, gurumate.httpd.check_running, self.proc)
    
    def test_No_listening_port(self):
        subprocess.check_output(shlex.split('sudo service apache2 stop'))
        self.assertRaises(ValidationError, gurumate.httpd.check_listening_port, self.port)
    
    def test_listening_port(self):
        gurumate.httpd.check_listening_port(self.port)
        
    def test_port_Not_in_ports_list(self):
        subprocess.check_output(shlex.split('sudo service apache2 stop'))
        self.assertNotIn(self.port, gurumate.httpd.get_listening_ports(self.proc))
    
    def test_port_in_ports_list(self):
        self.assertIn(self.port, gurumate.httpd.get_listening_ports(self.proc))
    