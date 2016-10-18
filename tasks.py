from invoke import task
from config import ApplicationConfig
from app.models import FirstModel,SecondModel
from app.extentions import db
from datetime import datetime,timedelta
import random, string
from app.app import create_app
import os
import logging
from logging.config import fileConfig

fileConfig('logging_config.ini')
logger = logging.getLogger('tasks')

@task
def build(ctx, type=None):
	
	logger.info('Job Started')
	create_app(ApplicationConfig).app_context().push()
	
	if type == 'aj':
		insertAdjecencyList()
	elif type == 'mp':
		insertMateriallizedPath()

	else: 
		print('Please Specify Data-Model Type!')
	

	logger.info('Job Finished')

def randomword(length):
   return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def insertAdjecencyList():
	last_id = db.session.query(FirstModel).order_by(FirstModel.id.desc()).first()
	NUM_RECORDS = int(os.getenv('NUM_RECORDS', 10))
	CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 10))
	
	logger.info('Number of Records to be Inserted: %i', NUM_RECORDS)
	logger.info('Chunk Size: %i', CHUNK_SIZE)
	
	if last_id is None:
		start_range = 1
		end_range = start_range + NUM_RECORDS
		parent_id = -start_range
	
	else:
		logger.info('Last Inserted Id: %i', last_id.id)
		start_range = last_id.id + 1
		end_range = start_range + NUM_RECORDS
		parent_id = last_id.parent_id
		
	
	for i in range(start_range , end_range):
		object_created_date = datetime.today() - timedelta(hours=i)
		object_updated_date = datetime.today() - timedelta(minutes=i)
		desc = randomword(i+10)
		title = randomword(5)

		if i%3 == 0:
			parent_id += 1

		model = FirstModel(
							i,
							object_created_date.strftime("%Y-%m-%d %H:%M:%S"), 
							object_updated_date.strftime("%Y-%m-%d %H:%M:%S"),
							parent_id,
							title, 
							desc
						   )
		
		db.session.add(model)
		
		
		if(i % CHUNK_SIZE == 0):
			logger.info('Commiting Session Rows')
			db.session.commit()

	db.session.commit()


def insertMateriallizedPath():
	last_id = db.session.query(SecondModel).order_by(SecondModel.id.desc()).first()
	NUM_RECORDS = int(os.getenv('NUM_RECORDS', 10))
	CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 10))
	
	logger.info('Number of Records to be Inserted: %i', NUM_RECORDS)
	logger.info('Chunk Size: %i', CHUNK_SIZE)
	
	if last_id is None:
		start_range = 1
		end_range = start_range + NUM_RECORDS
		parent_id = -1
		path = '1'
	
	else:
		logger.info('Last Inserted Id: %i', last_id.id)
		start_range = last_id.id + 1
		end_range = start_range + NUM_RECORDS
		parent_id = last_id.id
		path = str(last_id.path) + '.' +str(last_id.id)
		
	
	for i in range(start_range , end_range):
		object_created_date = datetime.today() - timedelta(hours=i)
		object_updated_date = datetime.today() - timedelta(minutes=i)
		desc = randomword(i+10)
		title = randomword(5)
		model = SecondModel(
							row_id = i,
							created_at = object_created_date.strftime("%Y-%m-%d %H:%M:%S"), 
							updated_at = object_updated_date.strftime("%Y-%m-%d %H:%M:%S"),
							parent_id = parent_id,
							title = title, 
							description = desc,
							path = path

						   )

		if i%3 == 0:
			parent_id += 1
			path = path + '.' +str(parent_id)
		

		
		
		db.session.add(model)
		
		if parent_id < 0:
			parent_id+=2
		
		
		if(i % CHUNK_SIZE == 0):
			logger.info('Commiting Session Rows')
			db.session.commit()

	db.session.commit()	
	