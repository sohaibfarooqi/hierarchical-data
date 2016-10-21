from .extentions import db
from .models import FirstModel,SecondModel
from sqlalchemy.orm import aliased
from flask import current_app as app
from sqlalchemy_utils import Ltree

class Helper:
	
	def getSubTree(parent_id):
		raise NotImplementedError()

	def getRootNodes():
		raise NotImplementedError()

	def getLeafNodes(parent_id = None):
		raise NotImplementedError()

	def getChildNodes(parent_id):
		raise NotImplementedError()

class AJHelper(Helper):
	
	def getSubTree(parent_id):
		"""
		SO: http://stackoverflow.com/questions/24779093/query-self-referential-list-relationship-to-retrieve-several-level-child
	    Docs: http://docs.sqlalchemy.org/en/rel_1_0/orm/query.html?highlight=cte#sqlalchemy.orm.query.Query.cte
		"""
		roots = FirstModel.query.filter(FirstModel.parent_id == parent_id).all()
		result_set = []
		for root in roots:
			included = db.session.query(
				FirstModel.id
				).filter(
				FirstModel.parent_id == root.id
				).cte(name="included", recursive=True)

			included_alias = aliased(included, name="parent")
			model_alias = aliased(FirstModel, name="child")

			included = included.union_all(
					db.session.query(
						model_alias.id
						).filter(
						model_alias.parent_id == included_alias.c.id
						)
						)
			model_ids = map(
				lambda _tuple: _tuple[0],
				[(root.id,)] + db.session.query(included.c.id).distinct().all(),
				)

			result =  FirstModel.query.filter(FirstModel.id.in_(model_ids)).all()
			result_set.extend(result)
		return result_set

    # Get all root nodes based on parent_id
	def getRootNodes():
		root = FirstModel.query.filter(FirstModel.parent_id == app.config["ROOT_ID"]).all()
		return root

	# Get all leaf nodes based on a parent_id. if no parent is provided it will return all leaf nodes.
	def getLeafNodes(parent_id = None):
		if parent_id is None:
			first_model_alias = aliased(FirstModel)
			return FirstModel.query.outerjoin(first_model_alias, FirstModel.id == first_model_alias.parent_id).filter(first_model_alias.parent_id == None).all()
		
		else:
			subtree = Helper.getSubTree(parent_id)
			for node in subtree:
				if node.id in [data.parent_id for data in subtree]:
					subtree.remove(node)
			return subtree

	# Get list of immediate child node based on parent_id
	def getChildNodes(parent_id):
		return FirstModel.query.filter(FirstModel.parent_id == parent_id).all()

class MPHelper(Helper):

	
	def getSubTree(id):
		"""
		Using Custom opertator in SQLAlchemy (Docs):
		http://docs.sqlalchemy.org/en/latest/core/custom_types.html#redefining-and-creating-new-operators
		SO: http://stackoverflow.com/questions/12212636/sql-alchemy-overriding
		"""
		subq = SecondModel.query.with_entities(SecondModel.path).filter(SecondModel.id == id).subquery()
		return SecondModel.query.filter(SecondModel.path.descendant_of(subq)).all()
