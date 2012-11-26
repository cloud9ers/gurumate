import unittest, os, pwd, subprocess
import gurumate

class TestUserOps(unittest.TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        self.groupname = "testgroup"

        os.system("useradd -U " + self.username)
        os.system("groupadd " + self.groupname)
        os.system("groupadd " + self.groupname + '1')
        os.system("adduser " + self.username + " " + self.groupname)
        dev_null = open('/dev/null', 'w')
        passwd = subprocess.Popen(['sudo', 'passwd', self.username], stdin=subprocess.PIPE,
                                  stdout=dev_null.fileno(),
                                  stderr=subprocess.STDOUT)
        passwd.communicate(((self.password + '\n') * 2).encode('utf-8'))
        
    def tearDown(self):
        os.system("userdel --f " + self.username)
        os.system("groupdel " + self.groupname)
        os.system("groupdel " + self.groupname + '1')
        
    def test_is_user(self):
      self.assertTrue(gurumate.user.is_user(self.username))
      self.assertFalse(gurumate.user.is_user("WrongUserName"))
    
    def test_is_group(self):
        self.assertTrue(gurumate.user.is_group(self.groupname))
        self.assertFalse(gurumate.user.is_group("WrongGroupName"))
                
    def test_is_in_group(self):
      self.assertTrue(gurumate.user.is_in_group(self.groupname, self.username))
      self.assertFalse(gurumate.user.is_in_group(self.groupname, "WrongUser"))
    
    def test_getuser_hash(self):
        import crypt
        shadow_line = gurumate.user.getuser_hash(self.username)
        salt = "$" + shadow_line.split("$")[1] + "$" + shadow_line.split("$")[2] + "$"
        hash = crypt.crypt(self.password, salt)
        self.assertEqual(hash, shadow_line)
        
    def test_authenticate(self):
        self.assertTrue(gurumate.user.authenticate(self.username, self.password))
        self.assertFalse(gurumate.user.authenticate(self.username, "WrongPassword"))
    
    def test_list_users(self):
        self.assertIn(self.username , gurumate.user.list_users())
    
    def test_list_groups(self):
        self.assertIn(self.groupname, gurumate.user.list_groups())
        self.assertNotIn(self.groupname , gurumate.user.list_groups(lambda g: g != self.groupname))
    
    def test_list_non_user_groups(self):
        self.assertNotIn(self.username , gurumate.user.list_non_user_groups())
        
    def test_users_in_group(self):
        self.assertIn(self.username, gurumate.user.users_in_group(self.groupname))
        
    def test_group_is_empty(self):
        self.assertTrue(gurumate.user.group_is_empty(self.groupname + '1'))
