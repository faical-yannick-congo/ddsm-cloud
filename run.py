"""Usage: run.py [--host=<host>] [--port=<port>] [--debug | --no-debug]

--host=<host>   set the host address or leave it to localhost.
--port=<port>   set the port number or leave it to 5000.

"""
from docopt import docopt
arguments = docopt(__doc__, version='0.1dev')

host = arguments['--host']
port = arguments['--port']
debug = not arguments['--no-debug']

from cloud import app
if not port: port = 5000
if not host: host = 'localhost'

app.run(debug=debug, host=host, port=int(port))