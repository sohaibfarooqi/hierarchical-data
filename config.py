import os


class ApplicationConfig:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    #SQLALCHEMY_ECHO=True #print SQL Query to Console
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('FLASK_DEBUG', False)
    SECRET_KEY = 'abcs'
    ROOT_ID = -1
    NUM_RECORDS = 100
    CHUNK_SIZE = 10
