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

@app.route('/tree/', defaults = {'parent_id': -1} , methods=['GET'])
@app.route('/tree/<int:parent_id>/' , methods=['GET'])
def get(parent_id):
	result_set = Helper.findAllTreeNodes(parent_id)
	return jsonify({'response': firstmodel_schemas.dump(result_set).data})

@app.route('/root' , methods=['GET'])
def get_root():
	result_set = Helper.findRootNodes()
	
	if type(result_set) is list:
		return jsonify({'response': firstmodel_schemas.dump(result_set).data})
	else:
		return jsonify({'response': firstmodel_schema.dump(result_set).data})
	