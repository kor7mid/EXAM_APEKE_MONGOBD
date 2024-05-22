# apps/__init__.py

import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from importlib import import_module
from apps.config import config_dict

# Initialize extensions
mongo = PyMongo()
login_manager = LoginManager()
mail = Mail()
moment = Moment()

def register_extensions(app):
    mongo.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.login_view = 'authentication_blueprint.login'

def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def create_app(config_class=None):
    app = Flask(__name__, instance_relative_config=True)

    # Load the configuration
    config_mode = os.getenv('FLASK_CONFIG_MODE', 'Debug')
    app_config = config_dict[config_mode]
    app.config.from_object(app_config)
    app.config.from_envvar('APP_CONFIG_FILE', silent=True)

    # Register extensions
    register_extensions(app)

    # Register blueprints
    register_blueprints(app)

    return app
