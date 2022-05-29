import os

dir = os.path.dirname(__file__)

PRIV_DIR = dir + os.sep + '..' + os.sep + 'priv' + os.sep
os.makedirs(PRIV_DIR, exist_ok=True)

PAGES_DIRECTORY = 'pages'