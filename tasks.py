from invoke import task
from config import ApplicationConfig
from app.models import FirstModel
from app.extentions import db
from datetime import datetime,timedelta
import random, string
from app.app import create_app


@task
def build(ctx):
	create_app(ApplicationConfig).app_context().push()
	for i in range(1,11):
		object_created_date = datetime.today() - timedelta(hours=i)
		object_updated_date = datetime.today() - timedelta(minutes=i)
		title = randomword(5)
		desc = randomword(i+10);
		model = FirstModel(
							i,
							object_created_date.strftime("%Y-%m-%d %H:%M:%S"), 
							object_updated_date.strftime("%Y-%m-%d %H:%M:%S"),
							i,
							title, 
							desc
						   )
		db.session.add(model)
	db.session.commit()

def randomword(length):
   return ''.join(random.choice(string.ascii_lowercase) for i in range(length))