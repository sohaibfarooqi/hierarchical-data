from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
from .models import AdjcencyListModel
def configure_extensions(app):
    db.init_app(app)
    Migrate(app, db)