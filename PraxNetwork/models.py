import string

#
#
# this entities are not object-mappers in the usual sense, they have to be dynamically mapped with attributes in functions
# an entity is a dictionary of functions
#
#
#
# 3 Types of Entities: 
# 0 degree freedom: nodes that are created through this application and provide important context, cannot be manipulated by user interaction
# 1 degree freedom: labeltype and attribute names are defined, content of attributes can vary
# 2 degree freedom: are defined dynamically, need to be accessed through their relations to Type 1 and 2 entities
#
#
#






####### Type 1 Entities #########




def get_metaconcept_entity():
	get_label = set_entity_label("Concept")
	def label(anyway = False):
		return get_label(anyway)
	def variable():
		return "metaconcept"
	def type():
		return "Node"
	def attributes():
		return ['id', 'name']
	return locals()





####### Type 2 Entities ##############


def get_datadoc_entity():
	get_label = set_entity_label("DataDoc")
	def label(anyway = False):
		return get_label(anyway)
	def variable():
		return "datadoc"
	def type():
		return "Node"
	def attributes():
		return ['id', 'name', 'content'] 
	return locals()


def get_interpretation_entity():
	get_label = set_entity_label("Interpretation")
	def label(anyway = False):
		return get_label(anyway)
	def variable():
		return "interpretation"
	def type():
		return "Node"
	def attributes():
		return ['id', 'content'] 
	return locals()


def get_sequence_entity():
	get_label = set_entity_label("Sequence")
	def label(anyway = False):
		return get_label(anyway)
	def variable():
		return "sequence"
	def type():
		return "Node"
	def attributes():
		return ['id', 'seqnumber', 'content']
	return locals()


def get_step_entity():
	get_label = set_entity_label("IStep")
	def label(anyway = False):
		return get_label(anyway)
	def variable():
		return "step"
	def type():
		return "Node"
	def attributes():
		return ['id', 'name']	
	return locals()


def get_concept_entity():
	get_label = set_entity_label("Concept")
	def label(anyway = False):
		return get_label(anyway)
	def variable():
		return "concept"
	def type():
		return "Node"
	def attributes():
		return ['id', 'name']
	return locals()



##### Type 3 Generic Nodes and Relations ##########



def get_relation_entity(var):
	get_label = set_entity_label("associated")
	def label(anyway = False):
		return get_label(anyway)
	def type():
		return "Relation"
	def variable():	
		return var
	def attributes():
		return ['id']
	return locals()

def get_node_entity(var, custom_label = ""):
	get_label = set_entity_label(custom_label)
	def label(anyway = False):
		return get_label(anyway)
	def type():
		return "Node"
	def variable():	
		return var
	def attributes():
		return ['id','name']
	return locals()




def generic_node_factory():
	i = 0
	def next_var(): 
		nonlocal i
		i += 1
		return get_node_entity("node" + str(i) + "_v")
	return next_var

def generic_relation_factory():
    i = 0
    def next_var(): 
        nonlocal i
        i += 1
        return get_relation_entity("rel" + str(i) +"_v")
    return next_var






### Helper Functions ###

def entityMap(entity,att): 
	return {'entity': entity, 'attributes': att}


def set_entity_label(eLabel):
	already_used = False
	def get_entity_label(anyway):
		nonlocal already_used
		if already_used is False or anyway is True:
			already_used = True	
			return eLabel
		else:
			return ""
	return get_entity_label


