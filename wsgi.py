from .app.app import create_app
from .config import ApplicationConfig
from flask import jsonify
from functools import wraps
from flask import request
from .app.helper import Helper
from .app.schema import firstmodel_schema, firstmodel_schemas

app = create_app(ApplicationConfig)
if __name__ == '__main__':
	app.run()

	