import collections

def dict_factory(cursor, row):
	"""This factory lets us access by index, string, or attribute.
	e.g. row[0] == row['item'] == row.item
	"""

	keys = []

	d = {}
	for idx, col in enumerate(cursor.description):
		keys.append(col[0])
		d[col[0]] = row[idx]

	def row_getitem(self, index):
		try:
			# Try numbered index first...
			return self.oldgetitem(index)
		except TypeError:
			try:
				# Probably a string key, try and get it...
				return getattr(self, index)
			except AttributeError:
				# Raise a KeyError, which feels Pythonic dict-like and intuitive
				raise KeyError
			except TypeError:
				# Raise a KeyError, which feels Pythonic dict-like and intuitive
				raise KeyError

	R = collections.namedtuple('Row', keys)
	R.oldgetitem = R.__getitem__
	R.__getitem__ = row_getitem

	ret = R(**d)

	return ret

class Database(object):
	def __init__(self, sql_engine, path, row_factory=None, *args, **kwargs):
		self.db = sql_engine.connect(path, *args, **kwargs)
		if row_factory == None:
			self.db.row_factory = dict_factory

	def execute(self, *args, **kwargs):
		"""Opens a new cursor and runs an execute"""
		c = self.db.cursor()
		return c.execute(*args, **kwargs)

	def executemany(self, *args, **kwargs):
		"""Opens a new cursor and runs an executemany"""
		c = self.db.cursor()
		return c.executemany(*args, **kwargs)

	def __getattr__(self, *args, **kwargs):
		"""Defers to underlying DB object, and then to cursor, if the method doesn't exist."""
		try:
			return self.__getattribute__(*args, **kwargs)
		except AttributeError:
			try:
				return getattr(self.db, *args, **kwargs)
			except AttributeError:
				c = self.db.cursor()
				return getattr(c, *args, **kwargs)

	def __del__(self):
		# Auto-commit DB in closing...
		if self.rowcount > 0:
			self.db.commit()
		self.db.close()
