import pathlib
import warnings
import cloudpickle
import perdict.utils as utils
import code

FILE = 'globals.cpkl'
FOLDER = pathlib.Path.home() / pathlib.Path(".perdict")

if not FOLDER.exists():
	FOLDER.mkdir()

class Perdict:
	"""
		Initialized with a dictionary-like object
	"""

	def __init__(self,filename=FOLDER/FILE,cache_mode=True):
		self.filename = pathlib.Path(filename)
		self.cache_mode = cache_mode
		if self.cache_mode:
			self.dic = self.load()

	def update(self):
		if not hasattr(self,"dic"):
			self.dic = self.load()
	def __getitem__(self,key):
		"""
			get value from disk
		"""

		key = utils.space_to_under(key)
		self.update()
		if key not in self.dic: 
			raise KeyError(f"Key {key} not in perdict")
		value = self.dic[key]
		
		return value
	
	def __setitem__(self,key,value):
		"""
			set value into dictionary and save as a pickle
		"""

		key = utils.space_to_under(key)
		self.update()

		if key in self.dic:
			warnings.warn(f"Overriding key {key} with a new value")
		self.dic[key] = value
		self.save()
			
	def __delitem__(self,key):
		"""
			delete value by its key
		"""

		key = utils.space_to_under(key)
		try:
			del self.dic[key]
		except (AttributeError,KeyError):
			pass

		self.save()

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

		self.update()
		return self

	def __exit__(self,*args):
		"""
			Should close the file when exit
		"""

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
		except EOFError:
			warnings.warn("[Loading Failed] The file might be corrupted, set dict to an empty dict")
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
		
	def __contains__(self,key):
		"""
			true or false regarding the key in dictionary
		"""
		
		key = utils.space_to_under(key)
		self.update()
		true_false = key in self.dic
		return true_false
	

	def __setattr__(self, key, value):
		"""
			when getitem fails, the key never saved on disk, so we can setitem
			However, string of test should not be equal with <Closed Dictionary> which 
			comes from shelf instance
		"""
		
		if key in self.__dict__:
			# If the attribute already exists, set its value
			self.__dict__[key] = value
			self.update()
			self.dic[key] = value
			self.save()
			print('in setattr')
			code.interact(local=dict(globals(),**locals()))
				
		else:
			# If the attribute doesn't exist, call the superclass method
			print('in setattr0')
			code.interact(local=dict(globals(),**locals()))
			super().__setattr__(key, value)

		
	
	def __repr__(self) -> str:
		"""
			representation of the instance
		"""
		return self.__class__.__name__

	def __eq__(self, value: object) -> bool:
		"""
			not implemented yet
		"""
		raise NotImplementedError
	
	def __hash__(self) -> int:
		"""
			not implemented yet
		
		"""
		raise NotImplementedError
	
	def __ne__(self, value: object) -> bool:
		"""
			not implemented yet
		"""
		raise NotImplementedError
	
	def __str__(self) -> str:
		"""
			string representation of the instance
		"""
		
		return str(self.dic)
	
if __name__=='__main__':  # pragma:no cover

	import os

	filename = 'test2.cpkl'
	local_pdic = Perdict(filename,cache_mode=False)
	local_pdic.fail_obj = "hello"
	os.remove(filename)
	
	


