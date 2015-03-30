"""Usage: run.py [--host=<host>] [--port=<port>] [--api | --view] [--debug | --no-debug]

--api           run the api app on port 5500
--view          run the view app on port 5000
--host			run the app on 127.0.0.1
--port=<port>   set the port number

"""
from docopt import docopt
arguments = docopt(__doc__, version='0.1dev')

host = arguments['--host']
port = arguments['--port']
debug = not arguments['--no-debug']

if arguments['--api']:
    from smt_api import app
    if not port: port = 5500
else:
    from smt_view import app
    if not port: port = 5000
if not host: host = '127.0.0.1'

#app.run(host=host, debug=debug, port=int(port))

