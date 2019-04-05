from flask import Flask
import os
from .extentions import configure_extensions, db
from .api import api_blueprint


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    configure_extensions(app)
    app.register_blueprint(api_blueprint)
    return app
