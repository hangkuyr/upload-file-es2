from flask import Flask, request, render_template, send_file, send_from_directory, Response, request, redirect, url_for, flash
from datetime import datetime, timedelta
from werkzeug.exceptions import RequestEntityTooLarge
import pandas as pd, os, sqlite3, numpy as np, time, werkzeug, os, json, io

app = Flask(__name__)

dir = os.path.dirname(__file__)
PRIV_DIR = dir + os.sep + '..' + os.sep + 'priv'