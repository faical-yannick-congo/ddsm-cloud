from flask import Flask
from .tools.converters import ObjectIDConverter
from flask.ext.mongoengine import MongoEngine

db = MongoEngine()

def setup_app(name, config=None):
    app = Flask(name)
    if config is None:
    	app.config.from_object('config')
    else:
    	app.config.from_object(config)
    app.debug = True

    # Flask-MongoEngine instance
    db.init_app(app)
    
    # Custom Converters
    app.url_map.converters['objectid'] = ObjectIDConverter

    return app

