import unittest, os, psutil, subprocess, shlex
import gurumate
class TestProcsOps(unittest.TestCase):
    def setUp(self):
        self.process = 'apache2'
        subprocess.check_output(shlex.split('sudo service apache2 start'))
        self.processtime = psutil.Process(os.getpid()).create_time
        self.processowner = 'root'
        self.procids = [int(pid) for pid in os.popen("sudo pgrep %s" % self.process).readlines()]
        
    def tearDown(self):
        subprocess.check_output(shlex.split('sudo service apache2 stop'))
    
    def test_is_running(self):
        self.assertTrue(gurumate.procs.is_running(self.process))
        
    def test_is_not_running(self):
        self.assertFalse(gurumate.procs.is_running("stopedprocess"))
        
    def test_is_running_by_ps(self):
        self.assertTrue(gurumate.procs.is_running_by_ps(self.process))

    def test_is_not_running_by_ps(self):
        self.assertFalse(gurumate.procs.is_running_by_ps("stopedprocess"))
        
    def test_get_pid(self):
        self.assertIn(gurumate.procs.get_pid(self.process), self.procids)
        
