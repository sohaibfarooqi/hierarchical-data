from flask import jsonify
from .result_processor import ResultProcessor, QueryHelper
from .mapper import Mapper

class ManagerFactory(object):
	
	def executeRequest(script_root, type, parent_id):
		result_set = ResultProcessor.evalResult(script_root,type,parent_id)
		return Response.format(result_set)


class Response():
	
	def format(result_set):
		return jsonify({"response": Mapper.map(result_set).data})


