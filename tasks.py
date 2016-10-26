from invoke import task
from config import ApplicationConfig
from app.models import FirstModel,SecondModel,NestedSetModel
from app.extentions import db
from datetime import datetime,timedelta
import random, string
from app.app import create_app
import os
import logging
from logging.config import fileConfig
from sqlalchemy_utils import Ltree


"""
author: Sohaib
dated: 2016-10-19
overview: This class help in building dummy records to perform benchmarking. It has options to switch between data models. Currently supported models are
Adjcency List and Materialized Path Views. use command invoke --help build to view all possible options.
"""


fileConfig('logging_config.ini')
logger = logging.getLogger('tasks')
NUM_RECORDS = int(os.getenv('NUM_RECORDS', 10))
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 10))

@task(help = {'type' : "Use --type aj and --type mp"})
def build(ctx, type=None):
	
	"""
	Insert Test data for benchmarking. See options for more details.
	"""
	
	logger.info('Job Started')
	create_app(ApplicationConfig).app_context().push()
	
	logger.info('Number of Records to be Inserted: %i', NUM_RECORDS)
	logger.info('Chunk Size: %i', CHUNK_SIZE)
	
	if type == 'aj':
		last_id = db.session.query(FirstModel).order_by(FirstModel.id.desc()).first()
		start,end_range,parent_id,path = getMeta(last_id)
		insertAdjecencyList(last_id,start,end_range,parent_id)
	
	elif type == 'mp':
		last_id = db.session.query(SecondModel).order_by(SecondModel.id.desc()).first()
		start,end_range,parent_id,path = getMeta(last_id)
		insertMateriallizedPath(last_id,start,end_range,parent_id,path)

	elif type == 'ns':
		last_id = db.session.query(NestedSetModel).order_by(NestedSetModel.id.desc()).first()
		start,end_range,parent_id,path = getMeta(last_id)
		insertNestedSet(last_id,start,end_range,parent_id,path)

	else: 
		logger.info('Please Specify Data-Model Type! Use --help for more info')
	

	logger.info('Job Finished')



def insertAdjecencyList(last_id,start_range,end_range,parent_id):
	
	for i in range(start_range , end_range):
		object_created_date = datetime.today() - timedelta(hours=i)
		object_updated_date = datetime.today() - timedelta(minutes=i)
		desc = randomword(i+10)
		title = randomword(5)

		if i%3 == 0:
			parent_id += 1

		model = FirstModel(
							id = i,
							created_at = object_created_date.strftime("%Y-%m-%d %H:%M:%S"), 
							updated_at = object_updated_date.strftime("%Y-%m-%d %H:%M:%S"),
							parent_id = parent_id,
							title = title, 
							description = desc
						   )
		
		db.session.add(model)
		
		if parent_id < 0:
			parent_id+=2
		
		if(i % CHUNK_SIZE == 0):
			logger.info('Commiting Session Rows')
			db.session.commit()

	db.session.commit()


def insertMateriallizedPath(last_id,start_range,end_range,parent_id,parent_path):

	for i in range(start_range , end_range):
		object_created_date = datetime.today() - timedelta(hours = i)
		object_updated_date = datetime.today() - timedelta(minutes = i)
		desc = randomword(i+10)
		title = randomword(5)
		model = SecondModel(
								row_id = i,
								created_at = object_created_date.strftime("%Y-%m-%d %H:%M:%S"), 
								updated_at = object_updated_date.strftime("%Y-%m-%d %H:%M:%S"),
								parent_id = parent_id,
								title = title, 
								description = desc,
								path = Ltree(parent_path  + "." + str(i))

							   )
		db.session.add(model)
		
		if parent_id < 0:
			parent_id+=2
			parent_path = parent_path + "." + str(i)
		
		if i % 3 == 0:
			parent_id += 1
			parent_object = SecondModel.query.filter(SecondModel.id == parent_id).first()
			if parent_object is not None:
				parent_path = str(parent_object.path)
		
		if(i % CHUNK_SIZE == 0):
			logger.info('Commiting Session Rows')
			db.session.commit()
		db.session.commit()

def insertNestedSet(last_id,start_range,end_range,parent_id,parent_path):
	
	"""
	- Inserting Tree
	"""

	for i in range(start_range , end_range):
		object_created_date = datetime.today() - timedelta(hours=i)
		object_updated_date = datetime.today() - timedelta(minutes=i)
		desc = randomword(i+10)
		title = randomword(5)

		if i%3 == 0:
			parent_id += 1

		model = NestedSetModel(
							id = i,
							created_at = object_created_date.strftime("%Y-%m-%d %H:%M:%S"), 
							updated_at = object_updated_date.strftime("%Y-%m-%d %H:%M:%S"),
							parent_id = parent_id,
							title = title, 
							description = desc
						   )
		
		db.session.add(model)
		
		if parent_id < 0:
			parent_id+=2
		
		if(i % CHUNK_SIZE == 0):
			logger.info('Commiting Session Rows')
			db.session.commit()

	db.session.commit()

	"""
	- Inserting Left and Right of nodes
	"""
	if last_id is None:
		parent_id = -1
	else:
		parent_id = last_id.id
	
	root = NestedSetModel.query.filter(NestedSetModel.parent_id == parent_id).first()
	#print(root.id)
	root.lft = 1
	db.session.add(root)
	db.session.commit()
	#print(root.lft)

	# child_nodes = NestedSetModel.query.filter(NestedSetModel.parent_id == root.id).all()
	# for key in child_nodes:
	# 	#print(key.id)
	# 	insertLftRgt(root, key)
	graph = {1: set([2]),
         	 2: set([3, 4, 5]),
         	 3: set([6, 7, 8]),
         	 4: set([9, 10])}
	
	sub_graph = dfs(graph, 3)
	print(sub_graph)

def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    if start in graph:
    	for next in graph[start] - visited:
    		dfs(graph, next, visited)
    return visited

#FIXME: Need terminating condition
def insertLftRgt(root, child):

	child.lft = root.lft + 1
	db.session.add(child)
	db.session.commit()
	child_nodes = NestedSetModel.query.filter(NestedSetModel.parent_id == child.id).all()

	for index, node in enumerate(child_nodes):
		insertLftRgt(child, node)
	
	child.lft = root.lft + 1
	child.rgt = child.lft + 1
	db.session.add(child)
	db.session.commit()
	print(child.id)
	insertLftRgt(root, child)
	




def randomword(length):
   return ''.join(random.choice(string.ascii_lowercase) for i in range(length))	


def getMeta(id):
	if id is None:
		end_range = 1 + NUM_RECORDS
		start = 1
		parent_id = -1
		path = 'None'
		return start,end_range,parent_id,path
	else:
		start = id.id + 1
		end_range = (id.id + 1) + NUM_RECORDS
		parent_id = id.parent_id
		parent_object = SecondModel.query.filter(SecondModel.id == parent_id).first()
		path = str(parent_object.path)
		return start,end_range,parent_id,path

