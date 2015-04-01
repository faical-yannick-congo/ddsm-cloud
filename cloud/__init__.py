import jinja2
import flask as fk
from ddsmdb.common.core import setup_app

app = setup_app(__name__)

# Templates
loader = jinja2.PackageLoader('cloud', 'templates')
template_env = jinja2.Environment(autoescape=True, loader=loader)
template_env.globals.update(url_for=fk.url_for)
template_env.globals.update(get_flashed_messages=fk.get_flashed_messages)

# Stormpath

from flask.ext.stormpath import StormpathManager

stormpath_manager = StormpathManager(app)

from . import views
from ddsmdb.common import models
from . import filters
