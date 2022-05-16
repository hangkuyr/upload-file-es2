PAGES_DIRECTORY = 'pages'

from app import*
from db import*

# importar automaticamente os arquivos escritos em \pages
import os, sys
PAGES_ABSOLUTE_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + os.sep + PAGES_DIRECTORY
sys.path.append(PAGES_ABSOLUTE_DIRECTORY)
for fileName in os.listdir(PAGES_ABSOLUTE_DIRECTORY):
	if fileName[-3:] == '.py':
		exec('from ' + fileName[:-3] + ' import*')

InitDB()
app.run(port=80, debug=True)
TerminateDB()