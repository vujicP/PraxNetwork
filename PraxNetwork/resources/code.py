from tastypie.resources import Resource
from tastypie.bundle import Bundle
from tastypie import fields
from ..models import *
from ..neo4j_layer import *
from .data_object import DataObject
import json

class CodeResource(Resource):

	data = fields.CharField(attribute='data')

	class Meta:
		resource_name = 'code'
		object_class = DataObject


	def detail_uri_kwargs(self, bundle_or_obj):
		return []

	def obj_get_list(self, bundle, **kwargs):
		return [DataObject(get_codes())]


	def obj_get(self, bundle, **kwargs):
		arg = kwargs['pk'].split("/")
		if len(arg) == 1:
			return DataObject(get_code_relations(arg[0]))
		if len(arg) == 2:
			if arg[0] == 'search':
				return DataObject(search_codes(arg[1]))
			else:
				return DataObject(get_code_origin(arg[1]))


	def obj_create(self, bundle, **kwargs):
		props = json.loads(bundle.request.body)
		if 'delete' in props:
			if 'intid' in props:
				return DataObject(delete_code(props['codeid'], props['intid']))
			else:
				return DataObject(delete_code_relation(props['relid']))
		return DataObject(create_rel_between_codes(props['id1'], props['id2']))



def get_codes(): 
	@processAction
	def graph():
		concept = get_concept_entity()
		interpretation = get_interpretation_entity()
		code = get_node_entity("code")
		return(match(interpretation,code,concept),
				where(exclude(entityMap(concept, { 'name': json.dumps('Concept') }))),
			   ret(code))
	return graph



def create_rel_between_codes(code1_id, code2_id): 
		gen = generic_node_factory()
		gen_r = generic_relation_factory()
		code1 = gen()
		code2 = gen()
		conn = gen_r()

		connectCodes = generic_action(match_indepedent(code1, code2),
											  where(entityMap(code1, {'id': code1_id}), entityMap(code2, {'id': code2_id})),
											  merge(code1, conn, code2),
											  ret(code1, code2))

		connectCodes()




def delete_code(code_id, int_id):
			gen = generic_node_factory()
			gen_r = generic_relation_factory()
			interpretation = get_interpretation_entity()	
			concept = gen()
			conn = gen_r()
			code = gen()
			deleteRel = generic_action(match(code,conn,interpretation),
							where(entityMap(code, {'id': code_id}),
							  	  entityMap(interpretation, {'id': int_id})),
							delete(conn))

			deleteRel()

			code = gen()
			deleteNode = generic_action(match(code),
							where(entityMap(code, {'id': code_id})),
							delete(code)) 

			deleteNode()



def delete_code_relation(rel_id):
			gen = generic_node_factory()
			gen_r = generic_relation_factory()
			code1 = gen()
			concept = gen()
			conn = gen_r()

			deleteRel = generic_action(match(code1,conn,concept),
				where(entityMap(conn, {'id': rel_id})),
				delete(conn))

			deleteRel()



def search_codes(searchstr): 
	@processAction
	def graph():
			concept = get_concept_entity()
			code = get_node_entity("code")

			return (match(code, concept),
					where(search(entityMap(code, {'name': json.dumps('(?i).*' + searchstr + '.*')})),
						  exclude(entityMap(code, [concept]))),
					ret(code))
	return graph


def get_code_origin(code_id):
	@processAction
	def graph():
		gen = generic_node_factory()
		code = gen()
		sequence = get_sequence_entity()
		interpretation = get_interpretation_entity()
		return (match(code, interpretation, sequence),
			   where(entityMap(code,{'id': code_id })),
			   ret(interpretation, sequence))
	return graph



def get_code_relations(code_id): 
	@processAction
	def graph():
		gen = generic_node_factory()
		gen_r = generic_relation_factory()
		code = get_node_entity("code")
		rel = gen_r()
		nextone = gen()
		interpretation = get_interpretation_entity()
		concept = get_concept_entity()

		return (match(code, rel, nextone),
				where(entityMap(code, {'id': code_id}),
					  exclude(entityMap(nextone, [interpretation, concept]))),
				ret(code, collect("rels", [rel, nextone])))
	return graph	