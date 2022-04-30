import os

dir = os.path.dirname(__file__)
__all__ = [i[:-3] for i in os.listdir(dir) if os.path.isfile(dir + os.sep + i) and i != '__init__.py']