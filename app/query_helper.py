from .extentions import db
from sqlalchemy.orm import aliased
from flask import current_app as app
from sqlalchemy_utils import Ltree

class QueryHelper():

	def executeQuery(model, action, id):
		return model.action(id)

class BaseQueryHelper(QueryHelper):
	
	# Get all root nodes. (Will be useful in case of Multiple trees)
	def getRootNodes(Model):
		root = Model.query.filter_by(Model.parent_id == app.config["ROOT_ID"]).all()
		return root

	# Get all leaf nodes based on a parent_id. if no parent is provided it will return all leaf nodes.
	def getLeafNodes(Model, parent_id = None):
		if parent_id is None:
			first_model_alias = aliased(Model)
			return Model.query.outerjoin(model_alias, Model.id == model_alias.parent_id).filter(model_alias.parent_id == None).all()
		
		else:
			subtree = QueryHelper.getSubTree(parent_id, Model)
			for node in subtree:
				if node.id in [data.parent_id for data in subtree]:
					subtree.remove(node)
			return subtree

	# Get list of immediate child nodes based on a parent_id
	def getChildNodes(Model, parent_id):
		
		if parent_id is None:
			#rasie Error
			return None
		else:
			return Model.query.filter(Model.parent_id == parent_id).all()

class SpecilizedHelper(QueryHelper):
	
	def getAjSubTree(Model, parent_id):

		"""
		SO: http://stackoverflow.com/questions/24779093/query-self-referential-list-relationship-to-retrieve-several-level-child
	    Docs: http://docs.sqlalchemy.org/en/rel_1_0/orm/query.html?highlight=cte#sqlalchemy.orm.query.Query.cte
		"""
		roots = Model.query.filter(Model.parent_id == parent_id).all()
		result_set = []
		for root in roots:
			included = db.session.query(
				Model.id
				).filter(
				Model.parent_id == root.id
				).cte(name="included", recursive=True)

			included_alias = aliased(included, name="parent")
			model_alias = aliased(Model, name="child")

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

			result =  Model.query.filter(Model.id.in_(model_ids)).all()
			result_set.extend(result)
		return result_set

	def getMpSubTree(id):
		
		"""
		Using Custom opertator in SQLAlchemy (Docs):
		http://docs.sqlalchemy.org/en/latest/core/custom_types.html#redefining-and-creating-new-operators
		SO: http://stackoverflow.com/questions/12212636/sql-alchemy-overriding
		"""
		subq = SecondModel.query.with_entities(SecondModel.path).filter(SecondModel.id == id).subquery()
		return SecondModel.query.filter(SecondModel.path.descendant_of(subq)).all()
	
	def LQuery(id, Model):
		
		if id is None:
			expr = Ltree('None.*')
		else:
			expr = Ltree("*." + str(id) + ".*") #Validation fails at this point. 
			return Model.query.filter(Model.path.lquery(expr)).all()
