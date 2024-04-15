import pathlib
import warnings
import cloudpickle
import perdict.utils as utils

FOLDER = pathlib.Path.home() / pathlib.Path(".pkg_name")

if not FOLDER.exists():
	FOLDER.mkdir()

DFLT_PATH = FOLDER / pathlib.Path("globals.ext")

class Perdict:
	"""
		Initialized with a dictionary-like object
	"""

	def __init__(self,filename=DFLT_PATH,cache_mode=True):
		self.filename = pathlib.Path(filename)
		self.cache = {}
		self.cache_mode = cache_mode
		
		self.update()
		
	def update(self):
		"""
			when Perdict does not have dict attribute, it will load the file and assign dic
		"""
		if not hasattr(self,"dic"):
			self.dic = self.load()

	def __getitem__(self,key):
		"""
			first try to get it from self.cache
		"""

		key = utils.space_to_under(key)
		try:
			value = self.cache[key]
			# print(f'get from cached-----{key}')
		except KeyError:
			self.dic = self.load()
			if key not in self.dic: 
				raise KeyError(f"Key {key} not in perdict")
			value = self.dic[key]
			if self.cache_mode:
				self.cache[key] = value
			# print(f'get from disk-------')
		
		return value
	
	def __setitem__(self,key,value):
		"""
			set value into dictionary and save as a pickle
		"""

		key = utils.space_to_under(key)
		if self.cache_mode:
			self.cache[key] = value
		
		else:
			if key in self.dic:
				warnings.warn(f"Overriding key {key} with a new value")
			self.dic[key] = value
			
	
	def __delitem__(self,key):
		"""
			delete value by its key
		"""

		key = utils.space_to_under(key)
		try:
			del self.dic[key]
		except (AttributeError,KeyError):
			pass
		try:
			del self.cache[key]
		except KeyError:
			pass
		self.save()

	def __iter__(self):
		"""
			yield next value
		"""

		for k in self.dic.keys():
			yield k
	
	def __len__(self):
		"""
			length of the dictionary
		"""
		
		return len(self.dic)
	
	def __enter__(self):
		"""
			entering in context manager
		"""
		return self

	def __exit__(self,*args):
		"""
			Should close the file when exit
		"""
		self.sync()

	def sync(self):
		"""
			sync the cache with dictionary and save
		"""
		self.dic.update(self.cache)
		self.cache = {}
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
		finally:
			f.close()
		# print("loading perdict...")
		return d

	def save(self):
		"""
			save dictionary
		"""

		f = open(self.filename, "wb")
		
		try:
			cloudpickle.dump(self.dic, f)
		except Exception:
			f.close()
			raise ValueError("Can not save the dictionary because of its values")
		f.close()
		
	def __contains__(self,key):
		"""
			true or false regarding the key in dictionary
		"""
		
		key = utils.space_to_under(key)
		true_false = key in self.dic or key in self.cache
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
				
			
		else:
			# If the attribute doesn't exist, call the superclass method
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

	class Temp:
		def __init__(self):
			self.x = open('ex.txt','w')

	
	filename = 'test2.cpkl'

	local_pdic = Perdict(filename,cache_mode=False)
	local_pdic.cache = {'x':"x_val"}
	local_pdic.sync()
	local_pdic.cache = 'cahnged'
	# local_pdic.x = 'x_val'
	# local_pdic.sync()
	# local_pdic.x = 'changed'
	import os
	os.remove(filename)
	
	


