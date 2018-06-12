from tastypie.resources import Resource
from tastypie.bundle import Bundle
from tastypie import fields
from ..models import *
from ..neo4j_layer import *
from .data_object import DataObject
import json


class InterpretationResource(Resource):

	data = fields.CharField(attribute='data')

	class Meta:
		resource_name = 'interpretation'
		object_class = DataObject


	def detail_uri_kwargs(self, bundle_or_obj):
		return []

	def obj_get_list(self, bundle, **kwargs):
		pass 


	def obj_get(self, bundle, **kwargs):
		arg = kwargs['pk'].split("/")
		if len(arg) == 2:
			return DataObject(get_int(json.dumps(arg[0]), arg[1]))


	def obj_create(self, bundle, **kwargs):
		props = json.loads(bundle.request.body)
		if 'intid' in props:
			return DataObject(update_int(json.dumps(props["content"]),props["intid"]))
		else: 
			return DataObject(create_int(json.dumps(props["content"]),props["seqid"],props["stepid"]))

def get_int(datadoc_name, step_id):
	@processAction 
	def graph():
		datadoc = get_datadoc_entity()
		sequence = get_sequence_entity()
		step = get_step_entity()
		interpretation = get_interpretation_entity()

		return (match((datadoc, sequence, interpretation),(step, interpretation)),
				where(entityMap(datadoc, {'name': datadoc_name}),
					  entityMap(step, {'id': step_id})),
				ret(interpretation, entityMap(sequence, {'id'}))
				) #todo seqid is still hardcoded!
	return graph


def create_int(content,seqid,stepid):
		
		gen_r = generic_relation_factory()
		interpretation = get_interpretation_entity()
		step = get_step_entity()
		sequence = get_sequence_entity()
		conn = gen_r()
		conn2 = gen_r()

		createInterpretation = generic_action(merge(entityMap(interpretation, { 'content': content })),
											   ret(entityMap(interpretation, { 'id' })))
		int_id = createInterpretation()

		
		interpretation = get_interpretation_entity()
		connectStepAndInterpretation = generic_action(match_indepedent(sequence, interpretation),
								  where(entityMap(sequence, {'id': seqid}), entityMap(interpretation, { 'id': int_id})),
								  merge(sequence, conn, interpretation),
								  ret(sequence, interpretation))

		interpretation = get_interpretation_entity()
		connectSequenceAndInterpretation = generic_action(match_indepedent(step, interpretation),
								  where(entityMap(step, {'id': stepid}), entityMap(interpretation, { 'id': int_id })),
								  merge(step, conn2, interpretation),
								  ret(step, interpretation))

		connectStepAndInterpretation()
		connectSequenceAndInterpretation()


def update_int(content, int_id):
	@processAction
	def graph():
			interpretation = get_interpretation_entity()

			return (match(interpretation), 
					where(entityMap(interpretation, {'id': int_id})),
					update(entityMap(interpretation, {'content': content})),
					ret(interpretation))

	return graph