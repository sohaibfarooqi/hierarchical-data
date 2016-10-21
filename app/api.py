from flask import Blueprint, jsonify
from functools import wraps
from .models import FirstModel
from .schema import firstmodel_schema, firstmodel_schemas, secondmodel_schema, secondmodel_schemas
from sqlalchemy.exc import IntegrityError
from .api_helper import Api, Resource
from .helper import Helper,MPHelper

api_blueprint = Blueprint('api_blueprint', __name__)


api = Api(api_blueprint)


@api.route('/subtree', 'parent_id')
def get_subtree (parent_id = -1):
	result_set = Helper.getSubTree(parent_id)
	return jsonify({'response': firstmodel_schemas.dump(result_set).data})

@api.route('/root')
def get_root():
	result_set = Helper.getRootNodes()
	if type(result_set) is list:
		return jsonify({'response': firstmodel_schemas.dump(result_set).data})
	else:
		return jsonify({'response': firstmodel_schema.dump(result_set).data})

@api.route('/leaf', 'parent_id')
def get_leaf(parent_id = None):
	result_set = Helper.getLeafNodes(parent_id)
	return jsonify({'response': firstmodel_schemas.dump(result_set).data})

@api.route('/child' , 'parent_id')
def get_child(parent_id = None):
	if parent_id is None:
		return jsonify({'response': 'Please Specify Parent Id'})	
	result_set = Helper.getChildNodes(parent_id)
	return jsonify({'response': firstmodel_schemas.dump(result_set).data})

@api.route('/subtree1', 'parent_id')
def get_subtree1 (parent_id = None):
	result_set = MPHelper.getSubTree(parent_id)
	return jsonify({'response': secondmodel_schemas.dump(result_set).data})

@api.route('/lquery', 'parent_id')
def get_subtree11 (parent_id = None):
	result_set = MPHelper.doLQuery(parent_id)
	return jsonify({'response': secondmodel_schemas.dump(result_set).data})