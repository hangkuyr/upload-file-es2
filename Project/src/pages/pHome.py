from app import*
from db import*
from cookies import*

MAX_SIZE = 30 * 2**20

FileCnt = 0
def GetUniqueFileId():
    '''
    Podemos usar o mesmo id para o arquivo e para o link do arquivo
    '''
    global FileCnt
    cur = FileCnt
    FileCnt += 1
    return str(cur)

@app.route('/', methods=['GET', 'POST'])
def mainPage():
    if request.method == 'GET':
        return render_template('index.html')
    else:

        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('invalidRequest.html')

        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return render_template('emptyFile.html')

        if len(file.read()) <= MAX_SIZE:
            file.seek(0)
            d = request.form
            attributes = 'title', 'desc', 'password'
            if all(i in d for i in attributes):
                id = GetUniqueFileId()
                title = d['title']
                desc = d['desc']
                password = d['password']
                db.saveFile(id, file, title, desc, password)
                resp = make_response(redirect('uploads/' + id))
                if password:
                    resp.set_cookie(GetCookieName(id), password)
                return resp
        return render_template('invalidRequest.html')
        