from app import*
from db import*

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
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return render_template('emptyFile.html')

        d = request.form
        title = d['title']
        desc = d['desc']
        id = GetUniqueFileId()
        SaveFile(id, file, title, desc)
        return redirect('uploads/' + id)