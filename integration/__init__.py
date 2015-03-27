from urllib2 import urlopen
from common.core import setup_app, db
# import os
# import nose
# from nose.tools import nottest
try:
	app = setup_app(__name__, 'integrate')
except:
	print "Something went wrong!!!"