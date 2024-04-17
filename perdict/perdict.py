import pathlib
import warnings

import cloudpickle

import perdict.utils as utils

FILE = "globals.cpkl"
FOLDER = pathlib.Path.home() / pathlib.Path(".perdict")

if not FOLDER.exists():
    FOLDER.mkdir()

LOCAL_ATRR = ["filename", "cache_mode", "dic"]


class Perdict:
    """
    Initialized with a dictionary-like object
    """

    def __init__(self, filename=FOLDER / FILE, cache_mode=True):
        self.filename = pathlib.Path(filename)
        self.cache_mode = cache_mode
        if self.cache_mode:
            self.dic = self.load()

    def update(self):
        """
        when cache_mode is false, dic attr was not created in init
        however, we need to create dic attr in some functions, so update is called
        from those functions
        """
        if not hasattr(self, "dic"):
            self.dic = self.load()

    def __getitem__(self, key):
        """
        get value from disk
        """

        key = utils.space_to_under(key)
        self.update()
        if key not in self.dic:
            raise KeyError(f"Key {key} not in perdict")
        value = self.dic[key]

        return value

    def __setitem__(self, key, value):
        """
        set value into dictionary and save as a pickle
        """

        key = utils.space_to_under(key)
        self.update()
        if key in self.dic:
            warnings.warn(f"Overriding key {key} with a new value")
        self.sync(key, value)

    def __delitem__(self, key):
        """
        delete value by its key
        """

        key = utils.space_to_under(key)
        self.update()
        try:
            del self.dic[key]
        except (AttributeError, KeyError):
            pass
        try:
            del self.__dict__[key]
        except (AttributeError, KeyError):
            pass

        self.save()

    def __delattr__(self, key):
        self.__delitem__(key)

    def __iter__(self):
        """
        yield next value
        """

        self.update()
        for k in self.dic.keys():
            yield k

    def __len__(self):
        """
        length of the dictionary
        """

        self.update()
        return len(self.dic)

    def __enter__(self):
        """
        entering in context manager
        """

        return self

    def __exit__(self, *args):
        """
        Should close the file when exit
        """
        self.update()
        self.save()

    def load(self):
        """
        load dictionary
        """

        if not self.filename.exists():
            return {}

        f = open(self.filename, "rb")
        try:
            d = cloudpickle.load(f)
        except Exception:
            warnings.warn(
                "[Loading Failed] The file might be corrupted, set dict to an empty dict"
            )
            d = {}
        finally:
            f.close()

        return d

    def save(self):
        """
        save dictionary
        """

        f = open(self.filename, "wb")

        try:
            cloudpickle.dump(self.dic, f)
        except Exception:
            raise ValueError("Can not save the dictionary because of its values")
        finally:
            f.close()

    def __contains__(self, key):
        """
        true or false regarding the key in dictionary
        """

        key = utils.space_to_under(key)
        self.update()
        true_false = key in self.dic
        return true_false

    def sync(self, key, value):
        """ """
        self.update()
        self.dic[key] = value
        self.save()

    def __getattr__(self, key):
        """
        first try to get the value from the dict of disk, then from dir
        """

        if not self.cache_mode:
            # to avoid max recursion. Cache_mode=False means that dic was not generated
            # in init
            self.dic = self.load()
        if key in self.dic:
            return self.dic[key]
        else:
            raise AttributeError(f"Perdict object has no attribute of {key}")

    def __setattr__(self, key, value):
        """
        if key not in LOCAL_ATTR, we save on disk
        """

        if key not in LOCAL_ATRR:
            self.sync(key, value)

        if key in self.__dict__:
            # If the attribute already exists, set its value
            self.__dict__[key] = value
        else:
            # If the attribute doesn't exist, call the superclass method
            super().__setattr__(key, value)

    def __repr__(self) -> str:
        """
        representation of the instance
        """
        return self.__class__.__name__

    def __eq__(self, other_dic: object) -> bool:
        """
        check equal with the other dictionary
        """

        if not isinstance(other_dic, dict):
            return False

        self.update()
        return sorted(self.dic.items()) == sorted(other_dic.items())

    def __hash__(self) -> int:
        """
        ensure that dictionaries with same content have same hash,
        even with the different order

        """
        self.update()
        try:
            result = hash(tuple(sorted(self.dic.items())))
        except TypeError:
            raise TypeError("unhashable object in the dictionary")
        return result

    def __ne__(self, other_dic: object) -> bool:
        """
        check inequality with the other dictionary,
        """

        if not isinstance(other_dic, dict):
            return True

        self.update()
        return sorted(self.dic.items()) != sorted(other_dic.items())

    def __str__(self) -> str:
        """
        string representation of the instance
        """

        return str(self.dic)
