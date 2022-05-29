from app import*
from db import*
import io
import filetype
from base64 import b64encode
from uploads import*

@app.route('/results/<id>')

def searchResult(id):
    return uploadsPath(id)