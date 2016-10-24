from flask import jsonify
from .schema import entity_schema, entity_schemas

class Response():
	
	"""
	Create Response from the retrieved result_set. Map the output using Mapper class.
	"""

	def create_response(result_set):
		try:
			mapper = Mapper.getMapper(result_set)
			final_response = jsonify({"data": mapper.dump(result_set).data})
			return final_response
		except ValueError:
			raise

	def create_error_response(error):
		if(err.has(args))
			return jsonify({"errors": error.args })
		else:
			return jsonify({"errors": "No Message Available"})

	def create_404_response(details):
		
		if details is None:
			return jsonify({"message": "No data available" })
		else:
			return Response.create_error_response(details)


class Mapper():
	
	"""
	Map the output according to result_set data-structure.
	"""
	def getMapper(instance):

		if type(instance) == list:
			return entity_schemas

		elif  type(instance) == object:
			return entity_schema

		else:
			raise ValueError('No Mapper found against {instance}'.format(instance = repr(instance)))
