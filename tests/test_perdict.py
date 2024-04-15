import unittest
import pathlib
import uuid
import tempfile
import os
import code

import cloudpickle

from perdict.perdict import Perdict,FOLDER


TEST_FILE = lambda: "tests/test_files/test_file.cpkl"

def dopen(filename, cache_mode=True):
	"""Open a persistent dictionary for reading and writing.
	"""
	pdic = Perdict(filename,cache_mode=cache_mode)
	return pdic

class Test_Perdict(unittest.TestCase):
    """
        1 test per function,
        each test will test all arguments of the function

    """
    @classmethod
    def setUpClass(cls):
        cls.filename = (
            pathlib.Path(tempfile.gettempdir())
            / f"tests.test_files.{uuid.uuid4()}"
        )
        cls.pdic = Perdict(cls.filename)
        # save the file
        try:
            os.rmdir(FOLDER)
        except:
            pass
        cls.pdic_default = Perdict()
        cls.pdic.save()
    @classmethod
    def tearDownClass(self):
        filename = str(self.filename)
        os.remove(filename)
    def test_initialization(self):
        """
            tests the initialization of the perdict, initialize 2 ways:
            without filename
            with filename
        """
        perdict = Perdict()
        perdict_with_file = Perdict(filename=self.filename)

        self.assertTrue(perdict.cache_mode)
        self.assertTrue(perdict_with_file.cache_mode)
    
    def test_setitem(self):
        """
            tests setitem using key, possible tests are following:
                1 key exists, override
                2 key does not exist
        """
        pdic = Perdict(self.filename)
        if "new_key" in pdic:
            del pdic["new_key"]
        old_size = os.path.getsize(self.filename)
        pdic["new_key"] = 10
        self.assertEqual(pdic["new_key"],10)
        # override
        pdic["new_key"] = 12
        self.assertEqual(pdic["new_key"],12)
        
        pdic['x']='x'*10000
        new_size = os.path.getsize(self.filename)
        self.assertTrue(new_size>old_size)

        pdic = Perdict(self.filename,cache_mode=False)
        pdic["new key"] = 10
        pdic["new_key"] = 12
        self.assertEqual(pdic["new_key"],12)

    def test_getitem(self):
        """
        
            tests getitem using key, possible tests are following:
                1 key exists
                2 key does not exist 
        """

        if "new_key" in self.pdic:
            self.assertEqual(self.pdic["new_key"],12)
            del self.pdic["new_key"]
        
        with self.assertRaises(KeyError):
            self.pdic["new_key"]
        
        # reset
        self.pdic["new_key"] = 12
        
        
    def test_delitem(self):
        """
            tests delitem, possible tests:
                1 key exists, delete the item
                2 key does not exist 
        """
        pdic = Perdict(self.filename)
        pdic['another_key'] = 40
        pdic.sync()
        old_size = os.path.getsize(self.filename)
        
        del pdic["another_key"]


        with self.assertRaises(KeyError):
            pdic["another_key"]
               
        new_size = os.path.getsize(self.filename)
        self.assertTrue(new_size<old_size)
    def test_iter(self):
        """
            tests iteration, returns next item one by one
        
        """
        self.pdic["current"] = 0
        # save 'current into disk
        self.pdic.sync()
        
        for k in self.pdic:
            
            if k=="current":
                x = self.pdic[k]
                break
        self.assertEqual(x,0)

    def test_len(self):
        """
            test lenght of dictionary
        """

        self.pdic["add_key"] = "hello"
        length_dict = len(self.pdic)
        self.assertTrue(length_dict>0)

    def test_enter_exit(self):
        """
            test context manager
        """

        with Perdict(self.filename) as local_pdic:
            local_pdic["context_key"] = "hello context key"
        
        self.assertEqual(self.pdic["context_key"],"hello context key")
        # after 
    def test_load(self):
        """
            test loading of the dictionary from disk
        """
        
        p = pathlib.Path("tests/test_files")
        if not p.exists():
            os.mkdir(p)
        new_file = p / "hello.cpkl"

        # delete file in case it exists
        try:
            os.remove(new_file)
        except OSError:
            pass
        new_dic = {"new_val":100}
        with open(new_file,"wb") as f:
            cloudpickle.dump(new_dic,f)
        
        local_pdic = Perdict(filename=new_file)
        del local_pdic["new_key"]
        # load the new_file again, so it should have the new_val
        local_pdic.load()
        self.assertEqual(local_pdic["new_val"],100)

        # reset
        try:
            os.remove(new_file)
        except OSError:
            pass
            
        

    
    def test_save(self):
        """
            test saving of the dictionary on disk
        """

        old_size = os.path.getsize(self.filename)
        local_pdic = Perdict(self.filename)
        # assigning value wont change the size of the file until we save it
        local_pdic["save_key"] = "hello saving"
        new_size = os.path.getsize(self.filename)
        self.assertEqual(old_size,new_size)
        local_pdic.sync()
        # now the new size would be larger than the old size
        
        new_size = os.path.getsize(self.filename)
        self.assertTrue(new_size>old_size)

    def test_contains(self):
        """
            test contains, where checks the key in dictionary
        """
        self.pdic["key_contains"] = lambda:"contains key assigned"
        self.assertTrue("key_contains" in self.pdic)


    def test_delattr(self):
        """
            test deleting attribute of instance
        """
    
    def test_key_with_space(self):
        """
            keys with space should be as same as key with underscore
        """

        key1 = "key space"
        key2 = "key_space"

        self.pdic[key1] = 130
        self.assertEqual(self.pdic[key1],self.pdic[key2])

    def test_repr(self):
        """
            test repr of the instance
        """

        repr(self.pdic)
    
    def test_eq(self):
        """
            currently does not implemented, test the notImplementedError
        """

        with self.assertRaises(NotImplementedError):
            self.pdic==self.pdic
    def test_hash(self):
        """
            currently does not implemented, test the notImplementedError
        """

        with self.assertRaises(NotImplementedError):
            hash(self.pdic)
    def test_ne(self):
        """
            currently does not implemented, test the notImplementedError
        """

        with self.assertRaises(NotImplementedError):
            self.pdic!=self.pdic


    def test_dopen(self):
        """
            filename is required for the open function
        """
        d = dopen(self.filename)
        self.assertTrue(d.cache_mode)
        old_size = os.path.getsize(self.filename)
        d['dopen_key'] = 'dopen'
        new_size = os.path.getsize(self.filename)
        # without d.sync(), file size does not change
        self.assertEqual(old_size,new_size)

        # with contextmanager, it sync automatically, so the size will be larger
        with dopen(self.filename) as pdic:
            pdic['dopen_key'] = 'dopen'
        
        new_size = os.path.getsize(self.filename)
        self.assertTrue(new_size>old_size)

    def test_setattr_delattr(self):
        """
            setattr eg, obj.x = 10
        """

        local_pdic = Perdict(self.filename,cache_mode=False)
        local_pdic.x = 'x value'
        self.assertEqual(local_pdic.x,"x value")
        del local_pdic.x
        with self.assertRaises(AttributeError):
            local_pdic.x


    def test_folder(self):
        """
            remove default folder
        """
        try:
            os.remove(FOLDER)
        except:
            pass
        pdic = Perdict()
        self.assertTrue(pdic.cache_mode)
    
    def test_save_fail(self):
        """
            try to save unpicklable object, such as, class without __reduce__ methods
        """

        class Temp:
            def __init__(self):
                self.x = open('ex.txt','w')
        
        pdic = Perdict("test.cpkl",cache_mode=False)
        pdic["fail_obj"] = Temp()

        with self.assertRaises(ValueError):
            pdic.sync()
        
        pdic.fail_obj = 'hello'

        #reset
        try:
            os.remove("test.cpkl")
        except:
            pass
        try:
            os.remove("ex.txt")
        except:
            pass
    
    def test_str(self):

        local_pdic = Perdict("test.cpkl",cache_mode=False)
        local_pdic["helo"] = 3
        str_repr = local_pdic.__str__()
        self.assertEqual(str_repr,"{'helo': 3}")

        # reset
        try:
            os.remove("test.cpkl")
        except:
            pass
        




        



### test usage tests, another file and class, test all functions of usage
### 


            
if __name__=='__main__':
    unittest.main()

