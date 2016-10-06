from .app.app import create_app
from .config import ApplicationConfig
from flask import jsonify
from functools import wraps
from flask import request
from .app.helper import Helper
from .app.schema import firstmodel_schema, firstmodel_schemas

app = create_app(ApplicationConfig)
if __name__ == '__main__':
	app.run()

@app.route('/subtree/', defaults = {'parent_id': -1} , methods=['GET'])
@app.route('/subtree/<int:parent_id>/' , methods=['GET'])
def get_subtree(parent_id):
	result_set = Helper.getSubTree(parent_id)
	return jsonify({'response': firstmodel_schemas.dump(result_set).data})

@app.route('/root/' , methods=['GET'])
def get_root():
	result_set = Helper.getRootNodes()
	
	if type(result_set) is list:
		return jsonify({'response': firstmodel_schemas.dump(result_set).data})
	else:
		return jsonify({'response': firstmodel_schema.dump(result_set).data})

@app.route('/leaf/', defaults = {'parent_id': None} , methods=['GET'])
@app.route('/leaf/<int:parent_id>' , methods=['GET'])
def get_leaf(parent_id = None):
	result_set = Helper.getLeafNodes(parent_id)
	return jsonify({'response': firstmodel_schemas.dump(result_set).data})
	