import unittest, subprocess, hashlib
import gurumate
import MySQLdb

class TestMySQLOps(unittest.TestCase):
    def setUp(self):
        #root
        self.rootname = "root"
        self.host = 'localhost'
        self.rootpasswd = ''
        #init databases
        self.init_dbs = ["information_schema", "mysql", "performance_schema"]
        self.init_users = ["root", "debian-sys-maint", ""]
        
        #user & database
        self.username = "testuser"
        self.passwd = "testpasswd"
        self.hashpass = "*" + (hashlib.sha1(hashlib.sha1(self.passwd).digest()).hexdigest()).upper()

        self.dbname = "testdb"
        self.tbname = "test_table"
        self.columns = "(testcl1 VARCHAR(20))"
        
        #MySQL connection 
        self.test_con = MySQLdb.connect(host=self.host, user=self.rootname, passwd=self.rootpasswd)
        self.cursor = self.test_con.cursor()

        #create Database with table
        self.cursor.execute("create database %s;" % self.dbname)
        self.cursor.execute("use %s;" % self.dbname)
        self.cursor.execute("CREATE TABLE %s %s" % (self.tbname, self.columns)) 
        
        #create User        
        self.cursor.execute("create user \'%s\'@\'localhost\' IDENTIFIED BY \'%s\';" % (self.username, self.passwd))
        self.cursor.execute("GRANT ALL PRIVILEGES ON %s.* to %s@localhost;" % (self.dbname, self.username))
        #create User without password
        self.cursor.execute("create user \'%s\'@\'localhost\';" % (self.username + '_2'))
        
        
    def tearDown(self): 
        #drop databases
        self.cursor.execute("show databases;")
        for dbname in [db.strip("'") for db in str(self.cursor.fetchall()).strip('((').strip(',))').split(",), (")] :
            if dbname not in self.init_dbs:
                self.cursor.execute("drop database %s;" % dbname)
        #drop users
        self.cursor.execute("select User from mysql.user;")
        for user in [username.strip("'") for username in str(self.cursor.fetchall()).strip('((').strip(',))').split(",), (")]:
            if user not in self.init_users:
                self.cursor.execute("drop user '%s'@'localhost'" % user)
        self.cursor.close()
                
    #Test Database methods 
    def test_database(self):
        self.assertIn(self.dbname, gurumate.mysql.database(self.rootname, self.rootpasswd))
        self.assertNotIn("wrongdbname", gurumate.mysql.database(self.rootname, self.rootpasswd))
        
    def test_database_exists(self):
        self.assertTrue(gurumate.mysql.database_exists(self.rootname, self.rootpasswd, self.dbname))
        self.assertFalse(gurumate.mysql.database_exists(self.rootname, self.rootpasswd, "wrongdbname"))
    
    def test_create_database(self):
        self.assertTrue(gurumate.mysql.create_database(self.rootname, self.rootpasswd, self.dbname + '_2'))
        self.assertTrue(gurumate.mysql.database_exists(self.rootname, self.rootpasswd, self.dbname + '_2'))
    
    def test_create_database_exists(self):
        self.assertRaises(MySQLdb.Error, gurumate.mysql.create_database, self.rootname, self.rootpasswd, self.dbname)
        
    def test_drop_database(self):
        self.assertTrue(gurumate.mysql.drop_database(self.rootname, self.rootpasswd, self.dbname))
    
    def test_drop_database_not_exists(self):
        gurumate.mysql.drop_database(self.rootname, self.rootpasswd, self.dbname)
        self.assertRaises(MySQLdb.Error, gurumate.mysql.drop_database, self.rootname, self.rootpasswd, self.dbname)
        
    
    #Test User Methods
    def test_users(self):
        self.assertIn(self.username, gurumate.mysql.users(self.rootname, self.rootpasswd))
        self.assertNotIn("wrongusername", gurumate.mysql.users(self.rootname, self.rootpasswd))
    
    def test_user_exists(self):
        self.assertTrue(gurumate.mysql.user_exists(self.rootname, self.rootpasswd, self.username))
        self.assertFalse(gurumate.mysql.user_exists(self.rootname, self.rootpasswd, "wrongusername"))
    
    def test_users_password(self):
        self.assertEqual(self.hashpass, gurumate.mysql.users_password(self.rootname, self.rootpasswd)[self.username])
        self.assertNotEqual('*wronghashpass', gurumate.mysql.users_password(self.rootname, self.rootpasswd)[self.username])
    
    def test_authenticate(self):
        self.assertTrue(gurumate.mysql.authenticate(self.rootname, self.rootpasswd, self.username, self.passwd))
        self.assertFalse(gurumate.mysql.authenticate(self.rootname, self.rootpasswd, self.username, 'wrongpass'))
    
    def test_no_passwd_set(self):
        self.assertTrue(gurumate.mysql.no_passwd_set(self.rootname, self.rootpasswd, self.username + '_2'))
        self.assertFalse(gurumate.mysql.no_passwd_set(self.rootname, self.rootpasswd, self.username))
        
    def test_set_new_password_for_user(self):
        self.assertTrue(gurumate.mysql.set_new_password_for_user(self.rootname, self.rootpasswd, self.username + '_2', self.passwd))
        self.assertTrue(gurumate.mysql.authenticate(self.rootname, self.rootpasswd, self.username + '_2', self.passwd))
        self.assertFalse(gurumate.mysql.authenticate(self.rootname, self.rootpasswd, self.username + '_2', ''))
        
    def test_add_new_user(self):
        self.assertTrue(gurumate.mysql.add_new_user(self.rootname, self.rootpasswd, self.username + '_3', self.passwd))
        self.assertTrue(gurumate.mysql.user_exists(self.rootname, self.rootpasswd, self.username + '_3'))
        
    def test_add_user_exists(self):
        gurumate.mysql.add_new_user(self.rootname, self.rootpasswd, self.username + '_3', self.passwd)
        self.assertRaises(MySQLdb.Error, gurumate.mysql.add_new_user, self.rootname, self.rootpasswd, self.username + '_3', self.passwd)
        
    
    def test_drop_new_user(self):
        self.assertTrue(gurumate.mysql.drop_user(self.rootname, self.rootpasswd, self.username))
        self.assertFalse(gurumate.mysql.user_exists(self.rootname, self.rootpasswd, self.username))
    
    def test_drop_user_not_exists(self):
        gurumate.mysql.drop_user(self.rootname, self.rootpasswd, self.username)
        self.assertRaises(MySQLdb.Error, gurumate.mysql.drop_user, self.rootname, self.rootpasswd, self.username)
        
    def test_users_host(self):
        self.assertEqual(self.host, gurumate.mysql.users_host(self.rootname, self.rootpasswd)[self.username + '_2'])
        
    def test_host(self):
        self.assertTrue(gurumate.mysql.host(self.rootname, self.rootpasswd, self.username, self.host))
    
    def test_show_grant(self):
        self.assertEqual(1, len(gurumate.mysql.show_grant(self.rootname, self.rootpasswd, self.username + '_2')))
        self.assertEqual(2, len(gurumate.mysql.show_grant(self.rootname, self.rootpasswd, self.username)))
        
    def test_grant_all_privileges(self):
        self.assertTrue(self.dbname in gurumate.mysql.show_grant(self.rootname, self.rootpasswd, self.username)[-1])
    
    #Test Tables
    def test_show_tables(self):
        self.assertIn(self.tbname, gurumate.mysql.show_tables(self.rootname, self.rootpasswd, self.dbname))
        self.assertNotIn("wrongtablename", gurumate.mysql.show_tables(self.rootname, self.rootpasswd, self.dbname))
        
    def test_table_exists(self):
        self.assertTrue(gurumate.mysql.table_exists(self.rootname, self.rootpasswd, self.dbname, self.tbname))
        self.assertFalse(gurumate.mysql.table_exists(self.rootname, self.rootpasswd, self.dbname, 'wrongtablename'))
    
    def test_create_table(self):
        self.assertTrue(gurumate.mysql.create_table(self.rootname, self.rootpasswd, self.dbname, self.tbname + '_2', self.columns))
        self.assertTrue(gurumate.mysql.table_exists(self.rootname, self.rootpasswd, self.dbname, self.tbname + '_2'))
        self.assertRaises(MySQLdb.Error, gurumate.mysql.create_table, self.rootname, self.rootpasswd, self.dbname, self.tbname + '_2', self.columns)

        
    def test_drop_table(self):
        self.assertTrue(gurumate.mysql.drop_table(self.rootname, self.rootpasswd, self.dbname, self.tbname))
        self.assertFalse(gurumate.mysql.table_exists(self.rootname, self.rootpasswd, self.dbname, self.tbname))    
        self.assertRaises(MySQLdb.Error, gurumate.mysql.drop_table, self.rootname, self.rootname, self.rootpasswd, self.dbname, self.tbname)
