from includes import*
from db import*

class TestDB:

	def setup_method(self):
		self.db = DB()

	def test_dbSaveFile_one_file(self):
		id = 'id teste'
		filename = 'teste.txt'
		title = 'título teste'
		desc = 'desc teste'
		data = b'teste bytes'
		password = 'teste password'
		self.db._saveFileImpl(id, filename, title, desc, data, password)
		dbItem = self.db.tryReadContents(id)
		assert dbItem.title == title

	def test_dbSaveFile_two_files(self):
		id = 'id teste'
		filename = 'teste.txt'
		title = 'título teste'
		data = b'teste bytes'
		self.db._saveFileImpl(id, filename, title, '', data, '')
		id2 = 'id teste 2'
		filename2 = 'teste2.txt'
		title2 = 'título teste 2'
		data2 = b'teste 2 bytes'
		self.db._saveFileImpl(id2, filename2, title2, '', data2, '')
		assert self.db.size() == 2
		

	def test_dbSorted(self):
		self.db._saveFileImpl('i1', 'f1', 't1', 'd1', b'b1', '')
		self.db._saveFileImpl('i2', 'f2', 't2', 'd2', b'b2', '')
		items = self.db.getItemsSortedByDate(1, 2)
		key = items[0][0]
		assert key == 'i1'

	def test_ListDoesNotShowPasswordProtectedFiles(self):
		self.db._saveFileImpl('i1', 'f1', 't1', 'd1', b'b1', 'p1')
		self.db._saveFileImpl('i2', 'f2', 't2', 'd2', b'b2', 'p2')
		items = self.db.getItemsSortedByDate(0, self.db.size())
		assert not len(items)

	def test_dbSize(self):
		self.db._saveFileImpl('i1', 'f1', 't1', 'd1', b'b1', 'p1')
		self.db._saveFileImpl('i2', 'f2', 't2', 'd2', b'b2', 'p2')
		assert self.db.size() == 2

	def test_deletePrivateDBItem_private_file(self):
		id = 'id teste'
		filename = 'teste.txt'
		title = 'título teste'
		desc = 'desc teste'
		data = b'teste bytes'
		password = 'teste password'
		self.db._saveFileImpl(id, filename, title, desc, data, password)
		self.db.deletePrivateDBItem(id)
		assert self.db.size() == 0

	def test_deletePrivateDBItem_public_file(self):
		id = 'id teste'
		filename = 'teste.txt'
		title = 'título teste'
		data = b'teste bytes'
		self.db._saveFileImpl(id, filename, title, '', data, '')
		id2 = 'id teste 2'
		filename2 = 'teste2.txt'
		title2 = 'título teste 2'
		data2 = b'teste 2 bytes'
		self.db._saveFileImpl(id2, filename2, title2, '', data2, '')
		self.db.deletePrivateDBItem(id)
		assert self.db.size() == 2

	def test_findFileByTitle(self):
		self.db._saveFileImpl('id', 'filename', 'title', 'desc', b'data', '')
		items = self.db.findPublicDBItemsByTitle('titl')
		assert len(items) == 1

	def test_findsFilesByTitle(self):
		self.db._saveFileImpl('id', 'filename', 'title', 'desc', b'data', '')
		self.db._saveFileImpl('id2', 'filename', 'title', 'desc', b'data', '')
		items = self.db.findPublicDBItemsByTitle('titl')
		assert len(items) == 2

	def test_findsSomeFilesByTitle(self):
		self.db._saveFileImpl('id', 'filename', 'title', 'desc', b'data', '')
		self.db._saveFileImpl('id2', 'filename', 'title', 'desc', b'data', 'password')
		self.db._saveFileImpl('id3', 'filename', 'title', 'desc', b'data', '')
		items = self.db.findPublicDBItemsByTitle('titl')
		assert len(items) == 2

	def test_notFindPrivateFiles(self):
		self.db._saveFileImpl('id2', 'filename', 'title', 'desc', b'data', 'password')
		items = self.db.findPublicDBItemsByTitle('titl')
		assert len(items) == 0