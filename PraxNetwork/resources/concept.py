from tastypie.resources import Resource
from tastypie.bundle import Bundle
from tastypie import fields
from ..models import *
from ..neo4j_layer import *
from .data_object import DataObject
import json

class ConceptResource(Resource):

	data = fields.CharField(attribute='data')

	class Meta:
		resource_name = 'concept'
		object_class = DataObject


	def detail_uri_kwargs(self, bundle_or_obj):
		return []

	def obj_get_list(self, bundle, **kwargs):
		return [DataObject(get_concepts())]


	def obj_get(self, bundle, **kwargs):
		return DataObject(get_abstractions(kwargs['pk']))


	def obj_create(self, bundle, **kwargs):
		props = json.loads(bundle.request.body)
		return DataObject(create_abstraction(json.dumps(props['concept']),json.dumps(props['code']),props["intid"]))


def get_concepts():
	@processAction
	def graph():
			concept = get_concept_entity()
			return(match(concept), ret(concept))
	return graph
			

def get_abstractions(int_id): 
	@processAction
	def graph():
			interpretation = get_interpretation_entity()
			abstraction = get_node_entity("abstraction")
			concept = get_concept_entity()
			code = get_node_entity("code")
			relation = get_relation_entity("relation")

			return (match((interpretation, abstraction, concept),(interpretation,code,relation,abstraction)),
					where(entityMap(interpretation, {'id': int_id})),
					ret(code, collect('rels', [abstraction, relation]))
					) 
	return graph



def create_abstraction(concept_name, code_name, int_id): 
		gen_r = generic_relation_factory()

		
		metaconcept = get_metaconcept_entity()
		createMetaConcept = generic_action(merge(entityMap(metaconcept,{ 'name': json.dumps('Concept')})),
														ret(entityMap(metaconcept,{ 'id'})))


		interpretation = get_interpretation_entity()
		concept = get_concept_entity()
		conn = gen_r()
		connectInterpretationAndConcept = generic_action(match(interpretation),
									where(entityMap(interpretation, {'id': int_id} )),
									merge(interpretation, conn, entityMap(concept, { 'name': concept_name})),
									ret(entityMap(concept, {'id'})))
		
		interpretation = get_interpretation_entity()
		code = get_node_entity("code", json.loads(concept_name))
		conn2 = gen_r()
		connectInterpretationAndCode = generic_action(match(interpretation),
									where(entityMap(interpretation, {'id': int_id} )),
									merge(interpretation, conn2, entityMap(code, {'name': code_name})),
									ret(entityMap(code, {'id'})))
		
		
		concept_id = connectInterpretationAndConcept() 
		code_id = connectInterpretationAndCode()
		meta_id = createMetaConcept()


		concept = get_concept_entity()
		code = get_node_entity("code", json.loads(concept_name))
		conn3 = gen_r()
		connectConceptAndCode = generic_action(match_indepedent(concept, code),
								where(entityMap(concept, {'id': concept_id}), entityMap(code, {'id': code_id})),
								merge(concept, conn3, code),
								ret(concept, code))

		concept = get_concept_entity()
		metaconcept = get_metaconcept_entity()
		conn4 = gen_r()
		connectConceptAndMetaConcept = generic_action(match_indepedent(concept, metaconcept),
									 where(entityMap(concept, {'id': concept_id}), entityMap(metaconcept, {'id': meta_id})),
									 merge(concept, conn4, metaconcept),
									 ret(concept,metaconcept))
		connectConceptAndCode() 
		connectConceptAndMetaConcept() 








	