from .extentions import db
from .models import FirstModel
from sqlalchemy.orm import aliased
from flask import current_app as app

class Helper:
	# Related SO: http://stackoverflow.com/questions/24779093/query-self-referential-list-relationship-to-retrieve-several-level-child
	# Docs: http://docs.sqlalchemy.org/en/rel_1_0/orm/query.html?highlight=cte#sqlalchemy.orm.query.Query.cte
	def findAllTreeNodes(parent_id = -1):
		root = FirstModel.query.filter(FirstModel.parent_id == parent_id).first()

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

		result = FirstModel.query.filter(FirstModel.id.in_(model_ids)).all()
		return result

	def findRootNodes():
		
		root = FirstModel.query.filter(FirstModel.parent_id == app.config["ROOT_ID"]).all()
		return root
