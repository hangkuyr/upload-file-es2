from app import*
from db import*
import io

# https://gist.github.com/Miserlou/fcf0e9410364d98a853cb7ff42efd35a

@app.route('/uploads/<path>', methods=['GET', 'POST'])
def serveFile(path):
    data = TryReadContents(path)
    if data is None:
        return render_template('invalidLink.html')
    if request.method == 'GET':
        '''
        Aqui, dependendo do tipo do arquivo (.png, .mp3, .wav, .txt) podemos renderizar
        de forma diferente
        '''
        print(data['title'])
        return render_template('file.html', path=path, title=data['title'], desc=data['desc'])
    else:
        return send_file(io.BytesIO(data['data']), attachment_filename=data['filename'], as_attachment=True)