import os

# get current directory this file is in
dir = os.path.dirname(__file__)

# add all files in current folder to our module
__all__ = [i[:-3] for i in os.listdir(dir) if os.path.isfile(dir + os.sep + i) and i != '__init__.py']