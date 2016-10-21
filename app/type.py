from .models import FirstModel, SecondModel

class Types():
	
	def getModel(type):
		if type == 'mp':
			return SecondModel()
		elif type == 'aj':
			return FirstModel()
		else:
			# Type Not Found
			return None
	
	def CheckType(Model):
		if isinstance(Model,FirstModel):
			return 'FirstModel'
		elif isinstance(Model,SecondModel):
			return 'SecondModel'
		else:
			#raise Error
			return None


