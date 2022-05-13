from flask import Flask, request, render_template, send_file, send_from_directory, Response, request, redirect, url_for, flash

# constants
dir = os.path.dirname(__file__)
PRIV_DIR = dir + os.sep + '..' + os.sep + 'priv' + os.sep

app = Flask(__name__)