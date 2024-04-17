import code
import os
import pathlib
import tempfile
import unittest
import uuid
import shutil

import cloudpickle

from perdict.perdict import FOLDER, Perdict

TEST_FILE = lambda: "tests/test_files/test_file.cpkl"


class Test_Perdict(unittest.TestCase):
    """
    1 test per function,
    each test will test all arguments of the function

    """

    @classmethod
    def setUpClass(cls):
        cls.filename = (
            pathlib.Path(tempfile.gettempdir()) / f"tests.test_files.{uuid.uuid4()}"
        )
        cls.pdic = Perdict(cls.filename)
        # save the file
        if FOLDER.exists():
            shutil.rmtree(FOLDER)
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
        self.assertEqual(pdic["new_key"], 10)
        # override
        pdic["new_key"] = 12
        self.assertEqual(pdic["new_key"], 12)

        pdic["x"] = "x" * 10000
        new_size = os.path.getsize(self.filename)
        self.assertTrue(new_size > old_size)

        pdic = Perdict(self.filename, cache_mode=False)
        pdic["new key"] = 10
        pdic["new_key"] = 12
        self.assertEqual(pdic["new_key"], 12)

    def test_getitem(self):
        """

        tests getitem using key, possible tests are following:
            1 key exists
            2 key does not exist
        """

        if "new_key" in self.pdic:
            self.assertEqual(self.pdic["new_key"], 12)
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
        pdic["another_key"] = 40
        old_size = os.path.getsize(self.filename)

        del pdic["another_key"]

        with self.assertRaises(KeyError):
            pdic["another_key"]

        new_size = os.path.getsize(self.filename)
        self.assertTrue(new_size < old_size)

    def test_iter(self):
        """
        tests iteration, returns next item one by one

        """
        self.pdic["current"] = 0

        for k in self.pdic:

            if k == "current":
                x = self.pdic[k]
                break
        self.assertEqual(x, 0)

    def test_len(self):
        """
        test lenght of dictionary
        """

        self.pdic["add_key"] = "hello"
        length_dict = len(self.pdic)
        self.assertTrue(length_dict > 0)

    def test_enter_exit(self):
        """
        test context manager
        """

        with Perdict(self.filename) as local_pdic:
            local_pdic["context_key"] = "hello context key"

        self.assertEqual(local_pdic["context_key"], "hello context key")
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
        new_dic = {"new_val": 100}
        with open(new_file, "wb") as f:
            cloudpickle.dump(new_dic, f)

        local_pdic = Perdict(filename=new_file)
        del local_pdic["new_key"]
        # load the new_file again, so it should have the new_val
        local_pdic.load()
        self.assertEqual(local_pdic["new_val"], 100)

        with open(new_file, "wb") as f:
            f.seek(2)
            cloudpickle.dump(local_pdic.dic, f)

        local_failed = Perdict(new_file, cache_mode=True)
        self.assertEqual(local_failed.dic, {})

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
        # now the new size would be larger than the old size

        new_size = os.path.getsize(self.filename)
        self.assertTrue(new_size > old_size)

    def test_contains(self):
        """
        test contains, where checks the key in dictionary
        """
        self.pdic["key_contains"] = lambda: "contains key assigned"
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
        self.assertEqual(self.pdic[key1], self.pdic[key2])

    def test_repr(self):
        """
        test repr of the instance
        """

        repr(self.pdic)

    def test_eq(self):
        """
        currently does not implemented, test the notImplementedError
        """

        other_dic = {"hello_eq": True}
        local_pdic = Perdict("test_eq.cpkl")
        local_pdic["hello_eq"] = True

        self.assertTrue(local_pdic == other_dic)
        self.assertFalse(local_pdic == [10])
        # reset
        try:
            os.remove("test_eq.cpkl")
        except Exception:
            pass

    def test_hash(self):
        """
        currently does not implemented, test the notImplementedError
        """

        def is_hashable(obj):
            try:
                hash(obj)
                return True
            except TypeError:
                return False

        local_pdic = Perdict("test_hash.cpkl")
        local_pdic["hello_hash"] = True
        self.assertTrue(is_hashable(local_pdic))
        # make it unhashable
        local_pdic["unhashable"] = [1, 2, 3]
        self.assertFalse(is_hashable(local_pdic))

        try:
            os.remove("test_hash.cpkl")
        except Exception:
            pass

    def test_ne(self):
        """
        currently does not implemented, test the notImplementedError
        """

        other_dic = {"hello_eq": True}
        local_pdic = Perdict("test_ne.cpkl")
        local_pdic["hello_ne"] = True

        self.assertTrue(local_pdic != other_dic)
        self.assertTrue(local_pdic != [10])
        # reset
        try:
            os.remove("test_ne.cpkl")
        except Exception:
            pass

    def test_setattr_delattr(self):
        """
        setattr eg, obj.x = 10
        """

        local_pdic = Perdict(self.filename, cache_mode=False)
        local_pdic.x = "x value"
        self.assertEqual(local_pdic.x, "x value")
        local_pdic.x = "y value now"
        self.assertEqual(local_pdic.x, "y value now")
        del local_pdic.x
        with self.assertRaises(AttributeError):
            local_pdic.x
    
    def test_getattr(self):
        """
            test getattr, eg oxj.x = 10; obj.x --> 10
        """

        local_pdic = Perdict(self.filename, cache_mode=False)
        local_pdic.x = 10
        print('in getaatt')
        self.assertEqual(local_pdic.x,10)
        self.assertFalse(local_pdic.cache_mode)



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
                self.x = open("ex.txt", "w")
                self.x.close()

        pdic = Perdict("test.cpkl", cache_mode=False)

        with self.assertRaises(ValueError):
            pdic["fail_obj"] = Temp()

        pdic.fail_obj = "hello"
        self.assertEqual(pdic.fail_obj, "hello")

        # reset
        try:
            os.remove("test.cpkl")
        except:
            pass
        try:
            os.remove("ex.txt")
        except:
            pass

    def test_str(self):

        local_pdic = Perdict("test.cpkl", cache_mode=False)
        local_pdic["helo"] = 3
        str_repr = local_pdic.__str__()
        self.assertEqual(str_repr, "{'helo': 3}")

        # reset
        try:
            os.remove("test.cpkl")
        except:
            pass


### test usage tests, another file and class, test all functions of usage
###


if __name__ == "__main__":
    unittest.main()
