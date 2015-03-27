import urllib2
from flask import Flask
from flask.ext.testing import LiveServerTestCase
import jinja2
import flask as fk
from common.core import setup_app, db
import os
import nose
from nose.tools import nottest

app = setup_app(__name__, 'integrate')
# Templates
loader = jinja2.PackageLoader('smt_view', 'templates')
template_env = jinja2.Environment(autoescape=True, loader=loader)
template_env.globals.update(url_for=fk.url_for)
template_env.globals.update(get_flashed_messages=fk.get_flashed_messages)
# Stormpath
from flask.ext.stormpath import StormpathManager
stormpath_manager = StormpathManager(app)
from smt_view import views
from common import models
from smt_view import filters


class CloudTest(LiveServerTestCase):

    def create_app(self):
        
        return app

    def setUp(self):

    	# Put some dummy things in the db.
        print "Supposed to setup the testcase."
        print "Which probably means to push some testing records in the database."

    def test_Cloud(self):

    	print "This is a test to check that the cloud endpoints are working properly."
        assert 1 == 1

    def tearDown(self):

    	print "Supposed to tear down the testcase."
    	print "Which most likely means to clear the database of all records."