from includes import*
from app import*
from flask import session

PNG_PATH = 'icon.png'
MP3_PATH = 'teste.mp3'

class TestUploads:

    def setup_method(self):
        self.app = CreateApp()
        self.client = self.app.test_client()
        self.d = self.getPostDictionary(PNG_PATH)
        self.dMP3 = self.getPostDictionary(MP3_PATH)
        self.TEST_PASSWORD = 'secret password'

    def getPostDictionaryWithPassword(self, fileName, password):
        return {
            'file': (Path(__file__).parent / 'files' / fileName).open('rb'),
            'title': 'teste title',
            'desc': 'teste desc',
            'password': password
        }

    def getPostDictionaryWithSpecificPath(self, path):
        return {
            'file': Path(path).open('rb'),
            'title': 'teste title',
            'desc': 'teste desc',
            'password': ''
        }

    def getPostDictionary(self, fileName):
        return self.getPostDictionaryWithSpecificPath(Path(__file__).parent / 'files' / fileName)

    def test_UploadPublicFileRedirectsToFilePage(self):
        response = self.client.post('/', data=self.d)
        assert response.status_code == 302

    def test_UploadPublicFileRendersCorrectTitle(self):
        response = self.client.post('/', data=self.d, follow_redirects=True)
        assert b'<h1>teste title</h1>' in response.data

    def test_UploadImageRendersImage(self):
        response = self.client.post('/', data=self.d, follow_redirects=True)
        assert b'<img src="data:;base64,iVBORw0KGgoAAAANSUhEU' in response.data

    def test_UploadFileShowsDownloadForm(self):
        response = self.client.post('/', data=self.d, follow_redirects=True)
        assert b"<input type=submit name=download value='Download File'>" in response.data

    def test_UploadMP3RendersBase64Audio(self):
        response = self.client.post('/', data=self.dMP3, follow_redirects=True)
        assert b'<source src="data:audio/mp3;base64,//OEZAAAAAAAAAAAAAA' in response.data

    def test_UploadPublicFileShowsOnRecent(self):
        self.client.post('/', data=self.dMP3, follow_redirects=True)
        response = self.client.get('/recent')
        assert b'teste title</a></td>' in response.data

    def test_PasswordProtectedUploadRequiresPasswordToAnotherClient(self):

        # um cliente salva um arquivo com senha
        postDict = self.getPostDictionaryWithPassword('fileMaxSize', self.TEST_PASSWORD)
        response = self.client.post('/', data=postDict)

        # link do arquivo
        url = response.location

        # outro cliente é pedido senha
        self.otherClient = self.app.test_client()
        assert b'<title>Password Protected File</title>' in self.otherClient.get(url).data

    def test_PasswordProtectedUploadSetCookieWithPassword(self):
        postDict = self.getPostDictionaryWithPassword('fileMaxSize', self.TEST_PASSWORD)
        response = self.client.post('/', data=postDict)
        COOKIE_SET_REQ = 'Set-Cookie'
        headers = response.headers
        assert COOKIE_SET_REQ in headers and self.TEST_PASSWORD in headers[COOKIE_SET_REQ]

    def test_HasDownloadButton(self):
        response = self.client.post('/', data=self.d)
        url = response.location
        response = self.client.get(url)
        assert b"<input type=submit name=download value='Download File'>" in response.data

    def test_CanDownloadPublicFile(self):

        BYTES = b'\x11\x12\x14'
        TEST_FILE_NAME = 'tmpFile'
        with open(TEST_FILE_NAME, 'wb') as f:
            f.write(BYTES)

        response = self.client.post('/', data=self.getPostDictionaryWithSpecificPath(TEST_FILE_NAME))
        url = response.location
        response = self.client.post(url, data={'download':''})
        os.remove(TEST_FILE_NAME)
        assert response.data == BYTES

    def test_Upload2PublicFiles(self):
        
        def getDictionary(path, title, desc):
            return {
            'file': (Path(__file__).parent / 'files' / path).open('rb'),
            'title': title,
            'desc': desc,
            'password': ''
        }

        TITLES = ['teste title 1', 'teste title 2']

        self.client.post('/', data=getDictionary(PNG_PATH, TITLES[0], 'teste desc 1'))
        self.client.post('/', data=getDictionary(MP3_PATH, TITLES[1], 'teste desc 2'))

        response = self.client.get('/recent')
        data = response.data
        assert all(bytes(title.encode()) + b'</a></td>' in data for title in TITLES)