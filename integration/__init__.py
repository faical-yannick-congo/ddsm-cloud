import urllib2
from flask import Flask
import flask as fk
from common.core import setup_app, db
import os
import nose
from nose.tools import nottest

app = setup_app(__name__, 'integrate')