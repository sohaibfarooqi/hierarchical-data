from flask import Blueprint, request, Request
from functools import wraps
from .api_helper import Api
from .manager_factory import RequestHandler

api_blueprint = Blueprint('api_blueprint', __name__)
api = Api(api_blueprint)

@api.route('/<script_path>', 'parent_id')
def process_request (script_path, parent_id = -1):
	
	result_set = RequestHandler.handleRequest(
												script_path, 
												type = request.args.get("type"),
												res = request.args.get("res"),
												parent_id = parent_id 
											)
	return result_set