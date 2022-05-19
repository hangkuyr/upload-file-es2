from app import*
from db import*
import io
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

        if request.method == 'GET':
            if db.isPasswordProtected(id):
                password = db.getFilePassword(id)
                if hasCorrectCookie(password):
                    return render_template('privateFile.html', dbItem=dbItem)
                else:
                    return render_template('passwordProtected.html')
            else:
                '''
                Aqui, dependendo do tipo do arquivo (.png, .mp3, .wav, .txt) podemos renderizar um template diferente
                '''
                return render_template('publicFile.html', title=dbItem.title, desc=dbItem.desc)
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
                        resp = make_response(render_template('privateFile.html', dbItem=dbItem))
                        resp.set_cookie(GetCookieName(id), password)
                        return resp
                    else:
                        return render_template('invalidPassword.html')
                if hasCorrectCookie(db.getFilePassword(id)):
                    return render_template('privateFile.html', dbItem=dbItem)
                return render_template('invalidRequest.html')
            else:
                return render_template('invalidMethod.html')