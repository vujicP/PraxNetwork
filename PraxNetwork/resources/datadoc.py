from tastypie.resources import Resource
from tastypie.bundle import Bundle
from tastypie import fields
from ..models import *
from ..neo4j_layer import *
from .data_object import DataObject
import json


class DataDocResource(Resource):

	data = fields.CharField(attribute='data')

	class Meta:
		resource_name = 'datadoc'
		object_class = DataObject


	def detail_uri_kwargs(self, bundle_or_obj):
		return []

	def obj_get_list(self, bundle, **kwargs):
		return [DataObject(get_all_datadocs())]


	def obj_get(self, bundle, **kwargs):
		if kwargs['pk'].isdigit():
			return DataObject(get_datadoc_byID(kwargs['pk']))
		else:
			return DataObject(get_datadoc_byName(json.dumps(kwargs['pk'])))


	def obj_create(self, bundle, **kwargs):
		props = json.loads(bundle.request.body)
		return DataObject(create_datadoc(json.dumps(props['name']), json.dumps(props['content'])))



def get_all_datadocs():
	@processAction
	def action():
		datadoc = get_datadoc_entity()
		return match(datadoc), ret(datadoc)
	return action


def get_datadoc_byID(uid):
	@processAction
	def action():
		datadoc = get_datadoc_entity()
		return (match(datadoc), 
				where(entityMap(datadoc,{
							'id': uid
						})
				  	  ), 
				ret(datadoc))
	return action

def get_datadoc_byName(name):
	@processAction
	def action():	
		datadoc = get_datadoc_entity()
		return (match(datadoc), 
				where(entityMap(datadoc, {
							'name': name
						})
				  	  ), 
				ret(datadoc))
	return action


def create_datadoc(name, content):
	@processAction
	def action():
		datadoc = get_datadoc_entity()
		return (merge(entityMap(datadoc,{
									'name': name,
									'content': content
								 })
					  ),
				ret(datadoc))
	return action


