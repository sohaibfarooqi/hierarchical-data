from .models import AdjcencyListModel
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def configure_extensions(app):
    db.init_app(app)
    Migrate(app, db)
