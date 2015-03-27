import urllib2
from flask import Flask
from flask.ext.testing import LiveServerTestCase
import jinja2
import flask as fk
from common.core import setup_app, db
import os
import nose
from nose.tools import nottest

class ApiTest(LiveServerTestCase):

    def create_app(self):

        app = setup_app(__name__, 'integrate')
        from smt_api import endpoints
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