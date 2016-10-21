from .schema import entity_schema, entity_schemas

class Mapper():
	def map(result_set):
		if result_set is not None:
			return entity_schema.dump(result_set)
		else:
			return entity_schemas.dump(result_set)

