import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = '33stanlake#'

DEBUG = True
TESTING = True
LIVESERVER_PORT = 5000

APP_TITLE = 'Sumatra Cloud'

VERSION = '0.1-dev'

MONGODB_SETTINGS = {
    'db': 'sumatra-flask',
    'host': '127.0.0.1',
    'port': 27017
}

STORMPATH_API_KEY_FILE = '../docker/stormpath/apiKey.properties'
STORMPATH_APPLICATION = 'sumatra-cloud'
STORMPATH_REDIRECT_URL = '/dashboard'


