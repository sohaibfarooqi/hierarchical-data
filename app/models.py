from .extentions import db
from sqlalchemy import func
from sqlalchemy_utils import LtreeType

class Entity:
    id = db.Column(db.Integer, primary_key=True)

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

class FirstModel(db.Model,Entity,TimestampMixin):
    parent_id = db.Column(db.Integer, index=True)
    title = db.Column(db.String)
    description = db.Column(db.String)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        if kwargs != {}:
            self.id = kwargs['id']
            self.created_at = kwargs['created_at']
            self.updated_at = kwargs['updated_at']
            self.parent_id = kwargs['parent_id']
            self.title = kwargs['title']
            self.description = kwargs['description']


class SecondModel(db.Model,Entity,TimestampMixin):
    parent_id = db.Column(db.Integer, index=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    path = db.Column(LtreeType)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.id = kwargs['row_id']
        self.created_at = kwargs['created_at']
        self.updated_at = kwargs['updated_at']
        self.parent_id = kwargs['parent_id']
        self.title = kwargs['title']
        self.description = kwargs['description']
        self.path = kwargs['path']

    



