from .extentions import db
from .models import FirstModel
from sqlalchemy.orm import aliased

class Helper:
	def doRecursiveQuery():
		#Root Element
		root = FirstModel.query.filter(FirstModel.parent_id == -1).first()

		#Get All Ids With Recursive Query
		included = db.session.query(
			FirstModel.id
			).filter(
			FirstModel.parent_id == root.id
			).cte(name="included", recursive=True)

		included_alias = aliased(included, name="parent")
		menu_alias = aliased(FirstModel, name="child")

		included = included.union_all(
				db.session.query(
					menu_alias.id
					).filter(
					menu_alias.parent_id == included_alias.c.id
					)
					)

		# Ids including root
		menu_ids = map(
			lambda _tuple: _tuple[0],
			[(root.id,)] + db.session.query(included.c.id).distinct().all(),
			)

		menus = FirstModel.query.filter(FirstModel.id.in_(menu_ids)).all()
		print (len(menus))
		return menus
