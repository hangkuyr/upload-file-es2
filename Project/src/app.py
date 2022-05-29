from flask import Flask, request, render_template, send_file, send_from_directory, Response, request, redirect, url_for, flash, make_response, Blueprint
from constants import*
from db import*

app = Blueprint('route_blueprint', __name__)

# importar automaticamente os arquivos escritos em \pages (que contém os roteamentos)
import os, sys
PAGES_ABSOLUTE_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + os.sep + PAGES_DIRECTORY
sys.path.append(PAGES_ABSOLUTE_DIRECTORY)
for fileName in os.listdir(PAGES_ABSOLUTE_DIRECTORY):
	if fileName[-3:] == '.py':
		exec('from ' + fileName[:-3] + ' import*')

def CreateApp():
    r = Flask(__name__)
    r.register_blueprint(app)
    return r