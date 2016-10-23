from . query_helper import QueryManager

class ResultProcessor:

	def evalResult(script_root,type, parent_id):
		"""
		Utilize QueryManager class to perform all steps to retrieve result.
		- get model instance
		- get method to be invoke
		- invoke method and return result.
		"""
		try:
			model = QueryManager.getModel(type)
			action = QueryManager.getAction(script_root, type)
			return QueryManager.executeQuery(model, action, parent_id)
		
		except ValueError as error:
			raise
