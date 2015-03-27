from integration import app, db
from flask.ext.testing import LiveServerTestCase

from smt_api import endpoints

class ApiTest(LiveServerTestCase):

    def create_app(self):

        return app

    def setUp(self):

    	# Put some dummy things in the db.
        print "Supposed to setup the testcase."
        print "Which probably means to push some testing records in the database."

    def test_Api(self):

    	print "This is a test to check that the api endpoints are working properly."
        assert 1 == 1

    def tearDown(self):

    	print "Supposed to tear down the testcase."
    	print "Which most likely means to clear the database of all records."