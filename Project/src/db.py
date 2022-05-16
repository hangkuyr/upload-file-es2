# Abstração do banco de dados

import json
from constants import*

DB_FILE = PRIV_DIR + 'db.json'

db = {}

def InitDB():
    try:
        global db
        with open(DB_FILE) as f:
            db = json.load(DB_FILE)
    except: # primeira vez
        pass

def TerminateDB():
    with open(DB_FILE, 'w') as f:
        json.dump(db, f)

def SaveFile(id, file, title='', desc=''):
    SaveFileImpl(id, file.filename, file.read(), title, desc)

def SaveFileImpl(id, filename, data, title, desc):
    d = {}
    d['filename'] = filename
    d['data'] = data
    d['title'] = title
    d['desc'] = desc
    db[id] = d

def TryReadContents(id):
    '''
    returns None if id is not in the database
    otherwise, returns a dictionary containing the data
    '''
    if id in db:
        return db[id]
    return None