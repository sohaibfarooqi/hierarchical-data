from flask import Blueprint, request, Request
from functools import wraps
from .api_helper import Api
from .manager_factory import ManagerFactory

api_blueprint = Blueprint('api_blueprint', __name__)


api = Api(api_blueprint)


@api.route('/<script_path>', 'parent_id')
def process_request (script_path, parent_id = -1):
	result_set = ManagerFactory.executeRequest(script_path, request.args.get("type"), parent_id)
	return result_set