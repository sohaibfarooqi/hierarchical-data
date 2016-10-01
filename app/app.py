from flask import Flask
import os
from .extentions import configure_extensions


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    configure_extensions(app)
    return app
