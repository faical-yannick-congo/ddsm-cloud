import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = '33stanlake#'

DEBUG = True

APP_TITLE = 'Sumatra Cloud'

VERSION = '0.1-dev'

MONGODB_SETTINGS = {
    'db': 'sumatra-flask',
    'host': '192.168.59.103',
    'port': 27017
}

STORMPATH_API_KEY_FILE = '~/.stormpath/apiKey.properties'
STORMPATH_APPLICATION = 'sumatra-cloud'
STORMPATH_REDIRECT_URL = '/dashboard'


