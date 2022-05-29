# Abstração do banco de dados

import json, threading
from timeUtils import*

class DBItem:
    def __init__(self, filename, title, desc, data, timestamp, password):
        self.filename = filename
        self.title = title
        self.desc = desc
        self.data = data
        self.timestamp = timestamp
        self.password = password

class DB:
    def __init__(self, path=None):
        if path is not None:
            with open(path) as f:
                self.db = json.load(f)
        else:
            self.db = {}

        self.mtx = threading.Lock() # para garantir atomicidade em algumas operações concatenadas

    def save(self, path):
        with open(path, 'w') as f:
            json.dump(self.db, f)

    def _saveFileImpl(self, id, filename, title, desc, data, password):
        timestamp = GetCurrentUTCTimestamp()
        self.db[id] = DBItem(filename, title, desc, data, timestamp, password)

    def saveFile(self, id, file, title='', desc='', password=''):
        self._saveFileImpl(id, file.filename, title, desc, file.read(), password)

    def deletePrivateDBItem(self, id):
        del self.db[id]

    def findPublicDBItemsByTitle(self, title):
        files = []
        for id in self.db:
            dbItem = self.db[id]
            if title in dbItem.title and dbItem.password == '':
                files.append([id, dbItem])
        return files

    def tryReadContents(self, id):
        '''
        returns None if id is not in the database
        otherwise, returns a dictionary containing the data
        '''
        if id in self.db:
            return self.db[id]
        return None

    def getItemsSortedByDate(self, m, M):
        '''
        Pega os items [m, M), onde m=0 é o item mais recente
        Se M > db.size()
        Retorna uma lista ordenada, onde cada elemento da lista é um par (id, db[id])
        '''

        sortedDict = {k: v for k, v in sorted(self.db.items(), key=lambda item:item[1].timestamp)[::-1]}

        listOfKeysSortedByTimestamp = list(sortedDict)
        
        # discard private files
        listOfKeysSortedByTimestamp = [i for i in listOfKeysSortedByTimestamp if not self.isPasswordProtected(i)]

        dbItems = []
        M = min(len(listOfKeysSortedByTimestamp), M)
        for i in range(m, M):
            key = listOfKeysSortedByTimestamp[i]
            dbItems.append([key, self.db[key]])
        return dbItems
    
    def size(self):
        '''
        Retorna o número de itens no db
        '''
        return len(self.db)

    '''
    Don't call with an invalid id
    '''
    def isPasswordProtected(self, id):
        return len(self.db[id].password)
    def getFilePassword(self, id):
        return self.db[id].password

from constants import*

DB_FILE = PRIV_DIR + 'db.json'

path = None
if os.path.exists(DB_FILE):
	path = DB_FILE
db = DB(path)