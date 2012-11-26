import unittest, os, tarfile, time
import subprocess, shlex, re
from pwd import getpwuid
import gurumate, random, string, ntpath

class TestFilesOps(unittest.TestCase):
    
    def setUp(self):
        N = 6
        self.dirname = "/tmp/" + ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))
        self.filename = self.dirname + '/' + ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N)) + '.txt'
        self.subdir = self.dirname + '/' + ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))
        self.tarfile = self.dirname + '/' + ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N)) + '.tar.gz'
        self.extractdir = self.dirname + '/extract_' + ntpath.basename(re.sub(r'\.tar.gz$', '', self.tarfile))
        self.symbolic_link = '%s_symln' % self.filename
        
        #create directory testdir
        os.mkdir(self.dirname)
        #create subdir in testdir
        os.mkdir(self.subdir)
        
        #Create file 
        open (self.filename, 'w+')
        #create Hidden File
        open(self.dirname + '/.' + ntpath.basename(self.filename) , 'w+')
        
        #Get file Owner 
        self.fileowner = getpwuid(os.stat(self.filename).st_uid).pw_name  
        #Change File permission
        self.permission = '777'
        subprocess.check_output(shlex.split('chmod %s %s' % (self.permission, self.filename)))
        #create symbolic link from testfile
        subprocess.check_output(shlex.split('ln -s %s %s' % (self.filename, self.symbolic_link)))
        
        
        #composed testfile1, testfile2.txt, subdir  in  testfiles.tar.gz     
        tar = tarfile.open(os.path.join(self.dirname, self.tarfile), "w:gz")
        for name in [self.filename,
                     self.dirname + '/.' + ntpath.basename(self.filename), 
                     self.subdir]:
            tar.add(name , arcname=os.path.basename(name))
        tar.close()
        #extract files in extractdir
        tar = tarfile.open(self.tarfile, "r:gz")
        tar.extractall(self.extractdir)
                
    def tearDown(self):
        import shutil
        shutil.rmtree(self.dirname)
    
    def test_get_ini_config_value(self):
        test_conf = "[test_section]\ntestkey = -testvalue "
        with open (self.filename, 'a') as f: f.write (test_conf)
        self.assertEqual('-testvalue',gurumate.files.get_ini_config_value(self.filename, 'test_section','testkey' ))
        
     
    def test_get_apache_config_value(self):
        #apachefile
        testmod_conf = '''
        <VirtualHost>\n
            <IfSection mod_test.c>\n
                    TestKey -testvalue\n
                         </IfSection>\n
        </VirtualHost>'''
        with open (self.filename, 'w') as f: f.write (testmod_conf)
        self.assertEqual("-testvalue", gurumate.files.get_apache_config_value(self.filename, 'IfSection', 'mod_test.c', 'TestKey'))
        
        
    def test_check_filemode(self):
        self.assertTrue(gurumate.files.check_filemode(self.filename, '0%s' % self.permission))
        
    def test_get_modification_datetime(self):
        with open (self.filename, 'a') as f: f.write ('test')
        modif_tim = os.stat(self.filename).st_mtime 
        self.assertEqual(modif_tim, gurumate.files.get_modification_datetime(self.filename))
        
    def test_is_recently_modified(self):
        with open (self.filename, 'a') as f: f.write ('test')
        self.assertTrue(gurumate.files.is_recently_modified(self.filename, 40))
    
    def test_check_exists(self):
        self.assertTrue(gurumate.files.check_exists(self.filename))
    
    def test_check_Not_exists(self):
        self.assertFalse(gurumate.files.check_exists("wrongFileName"))
        
    def test_get_source_of_symbolic_link(self):
        self.assertEqual(self.filename, gurumate.files.get_source_of_symbolic_link(self.symbolic_link))
        
    def test_get_permissions(self):
        self.assertEqual(self.permission, gurumate.files.get_permissions(self.filename))
    
    def test_get_owner(self):
        self.assertEqual(self.fileowner, gurumate.files.get_owner(self.filename))
    
    def test_all_lines_commented(self):
        with open (self.filename, 'a') as f: f.write ('#command1\n#command2\n#command3\n') #all line commented
        self.assertTrue(gurumate.files.all_lines_commented(self.filename)) 
    
    def test_Not_all_lines_commented(self):
        with open (self.filename , 'a') as f: f.write ('#command1\ncommand2\n#command3\n') #not all line commented
        self.assertFalse(gurumate.files.all_lines_commented(self.filename)) 
    
    def test_check_Nothidden(self):
        self.assertFalse(gurumate.files.check_hidden(self.filename))
    
    def test_check_hidden(self):
        self.assertTrue(gurumate.files.check_hidden('.' + self.filename))
    
    def test_list_dir(self):
        files, dirs = gurumate.files.list_dir(self.dirname)
        self.assertIn(ntpath.basename(self.subdir), dirs)
        self.assertIn(ntpath.basename(self.filename) , files)
        
    def test_search_all_files(self):
        files, dirs = gurumate.files.search_all_files(self.dirname, ntpath.basename(self.subdir))
        self.assertIn(self.subdir, dirs)
        self.assertEqual([], files)
    
    def test_search_by_extension(self):
        self.assertIn(self.filename, gurumate.files.search_by_extension(self.dirname, ".txt"))
        self.assertNotIn(self.tarfile, gurumate.files.search_by_extension(self.dirname, ".txt"))
    
    def test_is_Not_empty(self):
        with open (self.filename, 'a') as f: f.write ('test')
        self.assertFalse(gurumate.files.is_empty(self.filename))
    
    def test_is_empty(self):
        self.assertTrue(gurumate.files.is_empty(self.filename))
    
    def test_user_access(self):
        self.assertTrue(gurumate.files.user_access(self.filename, 'root'))

    def test_user_No_access(self):
        self.assertFalse(gurumate.files.user_access(self.filename, 'wronguser'))
    
    def test_extract_correct(self):
        self.assertTrue(gurumate.files.extract_correct(extractpath=os.path.join(self.dirname, self.extractdir), extractfiles=[ ntpath.basename(self.filename) , '.' + ntpath.basename(self.filename)], extractdirs=[ntpath.basename(self.subdir)]))
    
    def test_extract_Not_correct(self):
        self.assertFalse(gurumate.files.extract_correct(extractpath=os.path.join(self.dirname, self.extractdir), extractfiles=['wrongfile']))
        self.assertFalse(gurumate.files.extract_correct(extractpath=os.path.join(self.dirname, self.extractdir), extractfiles=[ self.filename + '1', self.filename + '2.txt'], extractdirs=[]))
