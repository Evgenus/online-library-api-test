from flask import Flask
from flask_login import LoginManager

from importlib import import_module

from .db import init_db
from .db import db
from .model import User
from .api import api_bp
from .logic import find_user_by_id


def load_user(user_id):
    return find_user_by_id(user_id)


def create_app(name, settings_mod_name=None, config_obj=None, **kwargs):
    app = Flask(name, **kwargs)

    config = app.config
    settings_mod_name = settings_mod_name or "settings"
    settings_mod = import_module(settings_mod_name)
    config.from_object(settings_mod)
    if config_obj:
        config.from_object(config_obj)

    init_db(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(load_user)

    app.register_blueprint(api_bp)

    return app
