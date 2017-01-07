class DictRow(object):
	def __init__(self,dtable,idx):
		self.dtable = dtable
		self.lut = dtable.lut
		self.ilut = dtable.ilut
		self.idx = idx

	def _dict_from_item(self,line):
		itemdict = { self.ilut[i] :itm for (i,itm) in enumerate(line)}
		return itemdict
	
	def keys(self):
		return self.lut.keys()	

	def get(self,key,restval):
		try:
			return self.dtable.table[self.idx][self.lut[key]]
		except KeyError:
			return restval
	
	def to_dict(self):
		line = self.dtable.table[self.idx]
		return self._dict_from_item(line)

	def to_list(self):
		return self.dtable.table[self.idx]

	def __getitem__(self,key):
		return self.dtable.table[self.idx][self.lut[key]]

	def __setitem__(self,key,val):
		self.dtable.table[self.idx][self.lut[key]]=val

	def __iter__(self):
		return DictRowIterator(self.dtable)

	def __len__(self):
		return len(self.lut)

	def __lt__(self,other):
		if isinstance(other,DictRow):
			return self.dtable.table[self.idx] < other.dtable.table[other.idx]
		else:
			raise TypeError("Not comparing with DictRow")
	
	def __gt__(self,other):
		if isinstance(other,DictRow):
			return self.dtable.table[self.idx] > other.dtable.table[other.idx]
		else:
			raise TypeError("Not comparing with DictRow")
	
	def __le__(self,other):
		if isinstance(other,DictRow):
			return self.dtable.table[self.idx] <= other.dtable.table[other.idx]
		else:
			raise TypeError("Not comparing with DictRow")

	def __ge__(self,other):
		if isinstance(other,DictRow):
			return self.dtable.table[self.idx] >= other.dtable.table[other.idx]
		else:
			raise TypeError("Not comparing with DictRow")

	def __eq__(self,other):
		if isinstance(other,DictRow):
			return self.dtable.table[self.idx] == other.dtable.table[other.idx]
		else:
			raise TypeError("Not comparing with DictRow")

	def __ne__(self,other):
		if isinstance(other,DictRow):
			return self.dtable.table[self.idx] != other.dtable.table[other.idx]
		else:
			raise TypeError("Not comparing with DictRow")

	def __repr__(self):
		return repr(self.to_dict())
		
class DictRowIterator(object):
	def __init__(self,dtable):
		self.idx = 0
		self.dtable = dtable
	
	def __iter__(self):
		return self
	
	def __next__(self):
		if self.idx >= len(self.dtable.lut):
			raise StopIteration
		item = self.dtable.ilut[self.idx]
		self.idx+= 1
		return item
	

class DictTableIterator(object):
	def __init__(self,dtable):
		self.idx = 0
		self.dtable = dtable
	
	def __iter__(self):
		return self
	
	def __next__(self):
		if self.idx >= len(self.dtable.table):
			raise StopIteration
		item = DictRow(self.dtable,self.idx)
		self.idx+= 1
		return item


class DictTable(object):
	def __init__(self,columns,content=None):
		self.columns = columns
		# column name : number
		self.lut = {k:v for (v,k) in enumerate(columns)}
		# number : column name
		self.ilut = {k:v for (k,v) in enumerate(columns)}
		self.table = []
		if content and len(content[0]) == len(self.lut):
			self.table = content

	def _item_from_dict(self,lidx,adict):
		self.table[lidx] = [None for _ in self.ilut]
		for (cidx,key) in self.ilut.items():
			self.table[lidx][cidx]=adict[key]
	
	
	def __getitem__(self,idx):
		if isinstance(idx,int):
			return DictRow(self,idx)
		elif isinstance(idx,slice):
			return DictTable(self.columns,self.table[idx])
		else:
			raise KeyError("Key must be int or slice")
	
	def __len__(self):
		return len(self.table)
	
	def __setitem__(self,idx,val):
		if isinstance(val, list):
			if len(val) != len(self.lut):
				raise TypeError("Trying to insert item with wrong number of columns")
			self.table[idx]=val
		elif isinstance(val, dict):
			self._item_from_dict(idx,val)
		elif isinstance(val, DictRow):
			self.table[idx]=val.to_list()
	def __iter__(self):
		return DictTableIterator(self)
	
	def __repr__(self):
		return "DictTable({} items, columns: {})".format(len(self),self.columns)

	def append(self,item):
		self.table.append([])
		self[-1]=item
	

	def key_sort(self,key):
		if isinstance(key, str):
			self.table.sort(key=lambda line: line[self.lut[key]])
		elif isinstance(key, list) or isinstance(key, tuple):
			self.table.sort(key=lambda line: tuple(line[self.lut[k]] for k in key))
		else:
			raise TypeError("Key must be string or list or tuple")

	
	def col_convert(self,col,conv):
		idx = self.lut[col]
		for row in self.table:
			row[idx] = conv(row[idx])
