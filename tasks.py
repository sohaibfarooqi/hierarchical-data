from invoke import task
from config import ApplicationConfig
from app.models import FirstModel
from app.extentions import db
from datetime import datetime,timedelta
import random, string
from app.app import create_app
import os

@task
def build(ctx):
	create_app(ApplicationConfig).app_context().push()
	last_id = db.session.query(FirstModel).order_by(FirstModel.id.desc()).first()
	
	RESULT_LIMIT = int(os.getenv('NUM_RECORDS', 10))

	if last_id is None:
		start_range = 1
		end_range = start_range + RESULT_LIMIT
		parent_id = start_range
	else:
		start_range = last_id.id + 1
		end_range = start_range + RESULT_LIMIT
		parent_id = last_id.id

	for i in range(start_range , end_range):
		object_created_date = datetime.today() - timedelta(hours=i)
		object_updated_date = datetime.today() - timedelta(minutes=i)
		title = randomword(5)
		desc = randomword(i+10);
		if i%3 == 0:
			parent_id+=1

		model = FirstModel(
							i,
							object_created_date.strftime("%Y-%m-%d %H:%M:%S"), 
							object_updated_date.strftime("%Y-%m-%d %H:%M:%S"),
							parent_id,
							title, 
							desc
						   )
		db.session.add(model)
	db.session.commit()

def randomword(length):
   return ''.join(random.choice(string.ascii_lowercase) for i in range(length))