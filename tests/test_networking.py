import unittest, socket, os, subprocess, shlex
import gurumate
class TestNetworkingOps(unittest.TestCase):
    def setUp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('google.com', 0))
        self.ip = s.getsockname()[0]
        self.port = int(os.popen("sudo cat /etc/apache2/ports.conf | grep Listen | cut -d ' ' -f2").readline().strip())
        self.hostname = subprocess.check_output(shlex.split("hostname")).strip()
        subprocess.check_output(shlex.split("sudo /etc/init.d/apache2 restart"))
    
    def tearDown(self):
        subprocess.check_output(shlex.split("sudo /etc/init.d/apache2 stop"))

    def test_is_port_accessible(self):
        self.assertTrue(gurumate.networking.is_port_accessible(self.ip, self.port))
        
    def test_is_port_inaccessible(self):
        subprocess.check_output(shlex.split("sudo /etc/init.d/apache2 stop"))
        self.assertFalse(gurumate.networking.is_port_accessible(self.ip, self.port))
        
    def test_check_hostname(self):
        self.assertTrue(gurumate.networking.check_hostname(self.hostname))
    
    