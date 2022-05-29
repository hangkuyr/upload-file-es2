from includes import*
from app import*
import flask

def test_CanCreateApp():
    app = CreateApp()
    assert type(app) == flask.app.Flask