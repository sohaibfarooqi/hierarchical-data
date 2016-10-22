from flask import jsonify
from .result_processor import ResultProcessor, QueryHelper
from .schema import entity_schema, entity_schemas

class RequestHandler():
	
	def handleRequest(script_root, **kwargs):
		result_set = ResultProcessor.evalResult(script_root,kwargs['type'],kwargs['parent_id'])
		
		if result_set != None:
			return Response.create_response(result_set, kwargs['res'])
		else:
			return 'None'

class Response():
	
	def create_response(result_set, res):
		result = FormatResult.format(result_set, res)
		mapper = Mapper.getMapper(res, result)
		final_response = jsonify({"response": mapper.dump(result_set).data})
		return final_response

class FormatResult():

	def format(result_set, res):
		
		if res == 'nc':
			pass	
		
		elif res == 'fl':
			return result_set
		
		else:
			#raise Error Response Formatter not implemented
			return None		

class NestedChild(FormatResult):
	
	def format(result_set):
		print("Not Implemented Yet.!")


class Mapper():
	
	def getMapper(res, instance):

		if res == 'fl' and type(instance) == list:
			return entity_schemas

		elif res == 'fl' and type(instance) == object:
			return entity_schema

		else:
			# No Mapper Found
			print("No Mapper Found")
			return None


