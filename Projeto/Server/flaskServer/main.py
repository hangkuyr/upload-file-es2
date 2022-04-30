'''
Inicialize o servidor:
py main.py [release_build]
onde [release_build] é 0 se estamos em modo de Debug, != 0 se Release
'''

from pch import*
from pages import*

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 0:
        release = int(sys.argv[1])
        if release:
            from waitress import serve
            #serve(app, threads=24)
            serve(app)
        else:
            app.run(port=80, debug=True)
    else:
        print("Invalid server initialization")