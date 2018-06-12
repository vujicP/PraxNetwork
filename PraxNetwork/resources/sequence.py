from tastypie.resources import Resource
from tastypie.bundle import Bundle
from tastypie import fields
from ..models import *
from ..neo4j_layer import *
from .data_object import DataObject
import json

class SequenceResource(Resource):

	data = fields.CharField(attribute='data')

	class Meta:
		resource_name = 'sequence'
		object_class = DataObject


	def detail_uri_kwargs(self, bundle_or_obj):
		return []

	def obj_get_list(self, bundle, **kwargs):
		pass


	def obj_get(self, bundle, **kwargs):
		return DataObject(get_seq(json.dumps(kwargs['pk'])))


	def obj_create(self, bundle, **kwargs):
		props = json.loads(bundle.request.body)
		return DataObject(create_seq(json.dumps(props['datadoc'])))



def create_seq(name):
		datadoc = get_datadoc_entity()
		getContent = generic_action(match(datadoc), 
						where(entityMap(datadoc, { 'name': name })),
						ret(entityMap(datadoc, {'content'})))

		content = getContent()
		if content is None:
			return ""
			
		split = content.split('\n')
		seqnumber = 1
		for seq in split:
			if seq != '':

				datadoc = get_datadoc_entity()
				gen_r = generic_relation_factory()
				conn = gen_r()
				sequence = get_sequence_entity()
				createSequence = generic_action(
							match(datadoc),
							where(entityMap(datadoc, {
									'name': name
								})),
							merge(datadoc,conn,entityMap(sequence, { "seqnumber": json.dumps(str(seqnumber)), "content": json.dumps(seq) })),
							ret(sequence)
							)
				createSequence()
				seqnumber += 1


def get_seq(name):
	@processAction
	def graph():
		datadoc = get_datadoc_entity()
		sequence = get_sequence_entity()
		gen_r = generic_relation_factory()
		conn = gen_r()
		return (match(datadoc,conn,sequence), 
				where(entityMap(datadoc, {
							'name': name 
						})
					 ),
				ret(sequence))
	return graph