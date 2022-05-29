OS_BACK = '..'
SRC_DIR = 'src'

from pathlib import Path

curDir = Path(__file__).parent.resolve()
pythonFilesDir = curDir / OS_BACK / SRC_DIR

import sys
sys.path.append(str(pythonFilesDir))

# alguns arquivos de teste
PNG_PATH = 'icon.png'
MP3_PATH = 'teste.mp3'