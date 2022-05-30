from includes import*
from app import*

class TestPages:

    def setup_method(self):
        self.app = CreateApp()
        self.client = self.app.test_client()

    def test_TitleIndex(self):
        response = self.client.get('/')
        assert b'<title>Upload File</title>' in response.data

    def test_IndexContainsRecents(self):
        assert b'<a href="/recent">Recent Uploads</a>' in self.client.get('/').data

    def test_IndexContainsSearch(self):
        assert b'<a href="/search">Search</a>' in self.client.get('/').data

    def test_IndexContainsAbout(self):
        assert b'<a href="/about">About</a>' in self.client.get('/').data

    def test_IndexDisallowsBigFiles(self):
        assert b'if (this.files[0].size > 31457280)' in self.client.get('/').data

    def test_IndexContainsAlert(self):
        assert b'alert("Erro: Arquivo Grande Demais\\nTamanho M' in self.client.get('/').data
        
    def test_IndexContainsPasswordField(self):
        assert b'Senha <input type=password name=password>' in self.client.get('/').data

    def test_IndexContainsSubmitButton(self):
        assert b'<input type="submit" value="Upload">' in self.client.get('/').data

    def test_SearchContainsDescription(self):
        assert b'que permite buscar arquivos' in self.client.get('/search').data

    def test_SearchContainsTopBar(self):
        assert b'<div class="topnav">' in self.client.get('/search').data

    def test_SearchContainsIcon(self):
        assert b'<link rel="icon" href="static/icon.png">' in self.client.get('/search').data

    def test_AboutContainsIcon(self):
        assert b'<a href="/about">About</a>' in self.client.get('/about').data

    def test_AboutContainsNavigationBar(self):
        assert b'<div class="topnav">' in self.client.get('/').data

    def test_RecentsContainsDescriptions(self):
        assert b'Uploads Recentes' in self.client.get('/recent').data