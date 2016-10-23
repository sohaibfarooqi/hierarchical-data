from flask import Blueprint, request, Request
from functools import wraps
from .route_handler import RouteHanlder
from .request_handler import RequestHandler


"""
Entry point of all requests.
"""

api_blueprint = Blueprint('api_blueprint', __name__)
api = RouteHanlder(api_blueprint)

@api.route('/<script_path>', 'parent_id')
def process_request (script_path, parent_id = -1):
	
	result_set = RequestHandler.handleRequest(
												script_path, 
												type = request.args.get("type"),
												parent_id = parent_id 
											)
	return result_set