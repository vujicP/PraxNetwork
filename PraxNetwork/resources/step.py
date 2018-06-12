from tastypie.resources import Resource
from tastypie.bundle import Bundle
from tastypie import fields
from ..models import *
from ..neo4j_layer import *
from .data_object import DataObject
import json


class StepResource(Resource):

	data = fields.CharField(attribute='data')

	class Meta:
		resource_name = 'step'
		object_class = DataObject


	def detail_uri_kwargs(self, bundle_or_obj):
		return []

	def obj_get_list(self, bundle, **kwargs):
		return 


	def obj_get(self, bundle, **kwargs):
		return DataObject(get_istep(json.dumps(kwargs['pk'])))


	def obj_create(self, bundle, **kwargs):
		props = json.loads(bundle.request.body)
		return DataObject(create_istep(json.dumps(props["datadoc"]),json.dumps(props["name"])))


def create_istep(datadoc_name, name):
		
		step = get_step_entity()	
		createStep = generic_action(merge(entityMap(step, {'name': name})),
												   ret(entityMap(step, {'id'})))

		step_id = createStep()
		

		step = get_step_entity()
		datadoc = get_datadoc_entity()
		gen_r = generic_relation_factory()
		conn = gen_r()	
		connectStepAndDataDoc = generic_action(match_indepedent(datadoc, step),
									  where(entityMap(step, {'id': step_id}), entityMap(datadoc, { 'name': datadoc_name})),
									  merge(step, conn, datadoc),
									  ret(step, datadoc))

		connectStepAndDataDoc()



def get_istep(name):
	@processAction
	def graph():
		datadoc = get_datadoc_entity()
		step = get_step_entity()
		gen_r = generic_relation_factory()
		conn = gen_r()
		return (match(datadoc,conn,step), 
				where(entityMap(datadoc, {
							'name': name
						})
					 ),
				ret(step))
	return graph