OS_BACK = '..'
SRC_DIR = 'src'

from pathlib import Path

curDir = Path(__file__).parent.resolve()
pythonFilesDir = curDir / OS_BACK / SRC_DIR

import sys
sys.path.append(str(pythonFilesDir))