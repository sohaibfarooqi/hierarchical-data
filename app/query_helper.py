from .extentions import db
from sqlalchemy.orm import aliased
from flask import current_app as app
from sqlalchemy_utils import Ltree
from .models import AdjcencyListModel, MaterializedPathModel, NestedSetModel


class QueryManager:

    """
    This Class defines factor methods to retrieve model and method to be invoke 
    based on query string params.
    """

    # defines dict of all avaliable methods in QueryHelper class. Type specific methods are nested in sub-dict
    __all_methods__ = {
        'child': 'getChildNodes',
        'leaf': 'getLeafNodes',
        'root': 'getRootNodes',
        'lquery': 'LQuery',
        'subtree': 'getSubTree'
    }

    def getModel(model_type):
        """
        Factory Method to retrieve model from 'type' param in query string. 
        Returns an instance of <type>Model class
        """
        if model_type == 'mp':
            return MaterializedPathModel

        elif model_type == 'aj':
            return AdjcencyListModel

        elif model_type == 'ns':
            return NestedSetModel

        else:
            raise ValueError('Model Type: {model_type} Not Implemented'.format(
                model_type=repr(model_type)))

    def getAction(script_root, model_type):
        """
        Factory Method to retrieve QueryHelper method based on script_root in Url.
        check __all_methods__ and returns if method is available otherwise raise Exception
        """

        if script_root in QueryManager.__all_methods__:
            return QueryManager.__all_methods__[script_root]

        else:
            raise ValueError("Action {script_root} Not Implemeted".format(
                script_root=repr(script_root)))

    def executeQuery(model, action, parent_id):
        return getattr(QueryHelper, action)(model, parent_id)


class QueryHelper():

    # Factory method to get Subtree based on type of model instance
    def getSubTree(*args):

        if args[0] == FirstModel:
            return SpecilizedQueryHelper.getAjSubTree(*args)

        elif args[0] == SecondModel:
            return SpecilizedQueryHelper.getMpSubTree(*args)

        elif args[0] == NestedSetModel:
            return SpecilizedQueryHelper.getNsSubTree(*args)

        else:
            raise ValueError("Subtree not implemented")

    # Get all root nodes. (Will be useful in case of Multiple trees)
    def getRootNodes(*args):
        root = args[0].query.filter(
            args[0].parent_id == app.config["ROOT_ID"]).all()
        return root

    # Get all leaf nodes based on a parent_id. if no parent is provided it will return all leaf nodes.
    def getLeafNodes(*args):
        if args[1] is None:
            first_model_alias = aliased(args[0])
            return args[0].query.outerjoin(model_alias, args[0].id == model_alias.parent_id).filter(model_alias.parent_id == None).all()

        else:
            subtree = QueryHelper.getSubTree(*args)
            for node in subtree:
                if node.id in [data.parent_id for data in subtree]:
                    subtree.remove(node)
            return subtree

    # Get list of immediate child nodes based on a parent_id
    def getChildNodes(*args):

        if args[1] is None:
            # rasie Error
            raise RuntimeError("Parent Id cannot be None")
        else:
            return args[0].query.filter(args[0].parent_id == args[1]).all()

    def LQuery(*args):

        if args[1] is None:
            expr = Ltree('None.*')
        else:
            # Validation fails at this point.
            expr = Ltree("*." + str(arg[1]) + ".*")
            return args[0].query.filter(args[0].path.lquery(expr)).all()


class SpecilizedQueryHelper(QueryHelper):

    def getAjSubTree(*args):
        """
        SO: http://stackoverflow.com/questions/24779093/query-self-referential-list-relationship-to-retrieve-several-level-child
    Docs: http://docs.sqlalchemy.org/en/rel_1_0/orm/query.html?highlight=cte#sqlalchemy.orm.query.Query.cte
        """
        roots = args[0].query.filter(args[0].parent_id == args[1]).all()
        result_set = []
        for root in roots:
            included = db.session.query(
                args[0].id
            ).filter(
                args[0].parent_id == root.id
            ).cte(name="included", recursive=True)

            included_alias = aliased(included, name="parent")
            model_alias = aliased(args[0], name="child")

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

            result = args[0].query.filter(args[0].id.in_(model_ids)).all()
            result_set.extend(result)
        return result_set

    def getMpSubTree(*args):
        """
        Using Custom opertator in SQLAlchemy (Docs):
        http://docs.sqlalchemy.org/en/latest/core/custom_types.html#redefining-and-creating-new-operators
        SO: http://stackoverflow.com/questions/12212636/sql-alchemy-overriding
        """
        subq = args[0].query.with_entities(args[0].path).filter(
            args[0].id == args[1]).subquery()
        return args[0].query.filter(args[0].path.descendant_of(subq)).all()

    def getNsSubTree(*args):
        """
        Related Artical: http://mikehillyer.com/articles/managing-hierarchical-data-in-mysql/
        """
        left, right = args[0].query.with_entities(
            args[0].lft, args[0].rgt).filter(args[0].id == args[1]).first()
        return args[0].query.filter(args[0].lft.between(left, right)).all()
