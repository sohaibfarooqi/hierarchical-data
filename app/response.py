from flask import jsonify
from .schema import entity_schema, entity_schemas

class Response():
	
	"""
	Create Response from the retrieved result_set. Map the output using Mapper class.
	"""

	def create_response(result_set):
		mapper = Mapper.getMapper(result_set)
		final_response = jsonify({"data": mapper.dump(result_set).data})
		return final_response

	def create_error_response(error):
		return jsonify({"errors": error.args })

	def create_404_response(details):
		
		if details is None:
			return jsonify({"message": "No data available" })
		else:
			return jsonify({"message": detals.args })


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
			# No Mapper Found
			print("No Mapper Found")
			return None
