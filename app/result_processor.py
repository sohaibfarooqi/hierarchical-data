from .types import QueryUtils
from . query_helper import QueryHelper

class ResultProcessor:

	def evalResult(script_root,type, parent_id):

		model = QueryUtils.getModel(type)
		action = QueryUtils.getAction(script_root)
		return QueryHelper.executeQuery(model, action, parent_id)