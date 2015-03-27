from flask.ext.testing import TestCase
from test_cloud import app, db
import os
import nose
from nose.tools import nottest

# from common.models import UserModel
# from common.models import ProjectModel
# from common.models import RecordModel

class CloudTest(TestCase):

    def create_app(self):
        
        return app

    def setUp(self):

    	# Put some dummy things in the db.
        print "Supposed to setup the testcase."
        print "Which probably means to push some testing records in the database."

    def test_MongoDb(self):

    	print "This is a custom test to check that Mongodb is working properly."
        assert 1 == 1

    def tear_Down(self):

    	print "Supposed to tear down the testcase."
    	print "Which most likely means to clear the database of all records."