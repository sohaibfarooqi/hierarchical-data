from .models import FirstModel, SecondModel

class QueryUtils():

	def getModel(type):

		if type == 'mp':
			return SecondModel
		elif type == 'aj':
			return FirstModel
		else:
			# Type Not Implemented
	def getAction(script_root):

		if script_root == 'lquery':
			return QueryHelper.doLQuery(parent_id, 'mp')
		
		elif script_root == 'subtree':
			return QueryHelper.getSubTree(Types.getModel(type), parent_id)
		
		elif script_root == 'root': 
			return QueryHelper.getRootNodes(Types.getModel(type))
		
		elif script_root == 'leaf':
			return QueryHelper.getLeafNodes(Types.getModel(type), parent_id)
		
		elif script_root == 'child':
			return QueryHelper.getChildNodes(Types.getModel(type), parent_id)
		
		else:
			#Method Not Implemented
			return None

class MethodFactory():
	factories = {}
    
    def registerMethod(id, shapeFactory):
        MethodFactory.factories.put[id] = shapeFactory
    addFactory = staticmethod(addFactory)
    
    # A Template Method:
    def getMethod(id):
        if not MethodFactory.factories.has_key(id):
            MethodFactory.factories[id] = \
              eval(id + '.Factory()')
        return MethodFactory.factories[id].create()
    getMethod = staticmethod(getMethod)


