from app import*
from db import*
import io
import filetype
from base64 import b64encode
from cookies import*

# https://gist.github.com/Miserlou/fcf0e9410364d98a853cb7ff42efd35a
@app.route('/uploads/<id>', methods=['GET', 'POST'])
def uploadsPath(id):
    with db.mtx:

        dbItem = db.tryReadContents(id)
        if dbItem is None:
            return render_template('invalidLink.html')

        def hasCorrectCookie(password):
            cookieName = GetCookieName(id)
            c = request.cookies
            return cookieName in c and c[cookieName] == password

        def getPageTemplate():
            '''
            Aqui, dependendo do tipo do arquivo (.png, .mp3, .wav, .txt) podemos renderizar um template diferente
            '''
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

        if request.method == 'GET':
            if db.isPasswordProtected(id):
                password = db.getFilePassword(id)
                if hasCorrectCookie(password):
                    return getPageTemplate()
                else:
                    return render_template('passwordProtected.html')
            else:
                return getPageTemplate()
                    
        else:

            def canSendFile():
                return not db.isPasswordProtected(id) or hasCorrectCookie(db.getFilePassword(id))

            if 'download' in request.form:
                if canSendFile():
                    return send_file(io.BytesIO(dbItem.data), attachment_filename=dbItem.filename, as_attachment=True)
                return render_template('invalidRequest.html')

            if db.isPasswordProtected(id):
                PASSWORD_NAME_IN_HTML = 'password'
                d = request.form
                if PASSWORD_NAME_IN_HTML in d:
                    password = db.getFilePassword(id)
                    if d[PASSWORD_NAME_IN_HTML] == password:
                        resp = make_response(getPageTemplate())
                        resp.set_cookie(GetCookieName(id), password)
                        return resp
                    else:
                        return render_template('invalidPassword.html')
                if hasCorrectCookie(db.getFilePassword(id)):
                    return getPageTemplate()
                return render_template('invalidRequest.html')
            else:
                return render_template('invalidMethod.html')