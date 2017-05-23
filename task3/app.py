from flask import Flask
from importlib import import_module

from .db import init_db


def create_app(name, settings_mod_name=None, config_obj=None, **kwargs):
    app = Flask(name, **kwargs)

    config = app.config
    settings_mod_name = settings_mod_name or "settings"
    settings_mod = import_module(settings_mod_name)
    config.from_object(settings_mod)
    if config_obj:
        config.from_object(config_obj)

    init_db(app)

    return app
