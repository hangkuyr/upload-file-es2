from includes import*
from app import*

class TestUploads:

    def setup_method(self):
        self.app = CreateApp()
        self.client = self.app.test_client()
        self.d = self.getPostDictionary('icon.png')
        self.dMP3 = self.getPostDictionary('teste.mp3')

    def getPostDictionary(self, fileName):
        return {
            'file': (Path(__file__).parent / 'files' / fileName).open('rb'),
            'title': 'teste title',
            'desc': 'teste desc',
            'password': ''
        }

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