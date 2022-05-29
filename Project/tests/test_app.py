from includes import*
from app import*
import flask

class TestApp:
    def setup_method(self):
        self.app = CreateApp()
        self.client = self.app.test_client()

    def test_AppIsInstantiated(self):
        assert type(self.app) == flask.app.Flask

    def test_IconIsPresent(self):
        assert b'<link rel="icon" href="static/icon.png">' in self.client.get('/').data

    def test_CheckTopBarShowsUploadFile(self):
        assert b'<a class="active" href="/">Upload File</a>' in self.client.get('/').data

    def test_CheckTopBarShowsRecentsTab(self):
        assert b'<a href="/recent">Recent Uploads</a>' in self.client.get('/').data

    def test_CheckTopBarShowsSearch(self):
        assert b'<a href="/search">Search</a>' in self.client.get('/').data

    def test_CheckTopBarShowsAbout(self):
        assert b'<a href="/about">About</a>' in self.client.get('/').data