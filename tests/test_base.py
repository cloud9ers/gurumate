import unittest, psutil, subprocess, shlex, os
import gurumate
from gurumate.base import ValidationError
from gurumate.base import ReturnException
from subprocess import CalledProcessError

class TestBaseOps(unittest.TestCase):
    def setUp(self):
        #fail and fill template messages
        self.fail_mssg = "test failling message"
        self.filltmp_mssg = {'hint' : 'test hint message'}
        
        #Running process
        self.run_proc_name = "apache2"
        subprocess.check_output(shlex.split("sudo /etc/init.d/apache2 start"))
        self.running_proc_command = "pgrep %s" % self.run_proc_name
        self.pid = [proc.pid for proc in psutil.process_iter() if proc.name == self.run_proc_name]
         
        #Local IP
        self.local_ip = os.popen("ifconfig eth0| grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'").read().strip()
    
    def teardown(self):
        subprocess.check_output(shlex.split("sudo /etc/init.d/apache2 stop"))
            
    def test_fail(self):
        self.assertRaises(ValidationError, gurumate.base.fail, self.fail_mssg)
        
    def test_fill_template(self):
        self.assertRaises(ReturnException, gurumate.base.fill_template, self.filltmp_mssg)
    
    def test_command_run(self):
        self.assertTrue(set(map(str, self.pid)).issubset(gurumate.base.run_command(self.running_proc_command).strip().split()))
    
    def test_command_not_run(self):   
        subprocess.check_output(shlex.split("sudo /etc/init.d/apache2 stop"))
        self.assertRaises(CalledProcessError, gurumate.base.run_command, self.running_proc_command)

    def test_get_pid_list(self):
        self.assertListEqual(self.pid, gurumate.base.get_pid_list(self.run_proc_name))
    
    def test_get_pid_of_stop_proc(self):
        subprocess.check_output(shlex.split("sudo /etc/init.d/apache2 stop"))
        self.assertListEqual([], gurumate.base.get_pid_list(self.run_proc_name))
    
    def test_get_run_proc_ports(self):
        apache_port = os.popen("cat /etc/apache2/ports.conf | grep Listen | cut -d: -f2| cut -d \" \" -f2").readline().strip()
        self.assertIn(int(apache_port), gurumate.base.get_listening_ports(self.run_proc_name)[0][-1])
    
    def test_stopped_proc_port(self):
        subprocess.check_output(shlex.split("sudo /etc/init.d/apache2 stop"))
        self.assertListEqual([], gurumate.base.get_listening_ports(self.run_proc_name))
        
    def test_get_local_ip(self):
        self.assertEqual(self.local_ip, gurumate.base.get_local_ip())
