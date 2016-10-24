from .result_processor import ResultProcessor
from .response import Response
from .schema import entity_schema, entity_schemas

class RequestHandler():
	
	"""
	First Step in request execution process.
	"""
	def handleRequest(script_root, **kwargs):
		
		try:
			result_set = ResultProcessor.evalResult(script_root,kwargs['type'],kwargs['parent_id'])
			
			if len(result_set) > 0:
				return Response.create_response(result_set)
			else:
				return Response.create_404_response(None)
		
		except (ValueError,RuntimeError) as error:
			return Response.create_error_response(error)


