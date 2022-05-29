from app import*
from db import*
import io
import filetype
from base64 import b64encode

@app.route('/results/<id>')

def searchResult(id):
    with db.mtx:

        dbItem = db.tryReadContents(id)
        if dbItem is None:
            return render_template('noResult.html')
        else:
            FILE_TEMPLATE = 'file.html'

            kind = filetype.guess(dbItem.data)

            d = {
                'title': dbItem.title,
                'desc': dbItem.desc
            }

            if kind is not None:
                if kind.extension in ['png', 'jpg']:
                    image = b64encode(dbItem.data).decode("utf-8")
                    d['img'] = image
                    d['specificTemplate'] = 'imageTemplate'
                if kind.extension in ['mp3']:
                    audio = b64encode(dbItem.data).decode("utf-8")
                    d['img'] = audio
                    d['specificTemplate'] = 'audioTemplate'
                    
            return render_template(FILE_TEMPLATE, **d)