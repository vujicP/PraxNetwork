import string
import json
from functools import reduce




### Match and Merge Path ###

def buildVarList(statement):
	def build(*args):
		return statement() + joinList(reduce(lambda a, b: a + [resolveArguments(b)], args, []))
	return build


def buildPath(statement):
	def build(*args):
		if(type(args[0]) is dict): 						#just one path sent	
			return statement() + combineVariablesToPath(args)
		else: 											#multiple paths sent
			path_var_gen = path_factory()
			return statement() + joinList(list(map(lambda a: combineVariablesToPath(a, path_var_gen()), args)))
	return build


def combineVariablesToPath(args, path_var = None):
	list_of_vars = reduce(lambda a, b: a + [resolveArguments(b)], args, [])
	path = createPathExpression(list_of_vars)
	if path_var is not None:
		path = path_var + "=" + path
	return path


def resolveArguments(a):
	if 'entity' not in a:	#user sends entity or otherwise dictionary/entityMap with entity and attributes
		return buildVariable(a)
	else:
		return buildVariable(a['entity'],a['attributes'])


def createPathExpression(list_of_vars):
		#todo: implement directions
		return reduce(lambda a, b: a + ("--" + b if (a.endswith(")") and b.startswith("(")) else "-" + b), list_of_vars)


def path_factory():
    i = 0
    def next_var(): 
        nonlocal i
        i += 1
        return "path" + str(i)
    return next_var



### Where Clauses ###


def buildWhereClause(statement):
	def build(list_of_clauses):
		#tdo implement OR etc.
		return statement() + " AND ".join(list_of_clauses)
	return build


def notEqual(build):
	@buildArgs
	def setClauses(list_of_values):
		return build(resolveListOfClauses(list_of_values, "{0} <> {1}", "NOT "))
	return setClauses

def equal(build):
	@buildArgs
	def setClauses(list_of_values):
		return build(resolveListOfClauses(list_of_values, "{0} = {1}"))
	return setClauses

def search(build):
	@buildArgs
	def setClauses(list_of_values):
		return build(resolveListOfClauses(list_of_values, "{0} =~ {1}"))
	return setClauses


def resolveListOfClauses(clauses, op, mod = None):
	retlist = []
	for c in clauses:
		if 'attribute' in c:
			retlist.append(op.format(c['attribute'], c['value']))
		elif 'variable' in c:
			var = addProp(c['variable'], c['label'])
			if mod is not None:
				var = mod + var
			retlist.append(var)
		else:
			retlist.append(c['resolved'])
	return retlist



def buildArgs(set_clauses):
	def build(*args):
		return set_clauses(reduce(lambda a, b: a + resolveFilterArgs(b), args, []))  
	return build

def resolveFilterArgs(a):
	retlist = []
	if 'entity' in a and type(a['attributes']) is list:
		for l in a['attributes']:
			retlist.append({"variable": a['entity']['variable'](), "label": l['label'](True)})
	elif 'entity' in a:	
		for key, value in a['attributes'].items():
			retlist.append({"attribute": addAttributeToVariable(a['entity']['variable'](), key), "value": value})
	else: 
		retlist.append({"resolved": a})

	return retlist	



### Return Values ####



def setCollectVariable(build_variables):
	def set(variable, entities):
		return build_variables(*entities) +  " as " + variable
	return set


def updateValues(statement):
	@equal
	def update(list_of_assignments):
		return statement().format(joinList(list_of_assignments))
	return update


def buildVariablesToProcess(statement):
	def build(*args):
		return statement().format(joinList([resolveReturnValues(arg) for arg in args]))	
	return build


def resolveReturnValues(arg):
	if 'entity' in arg:
		return joinList([addAttributeToVariable(arg['entity']['variable'](), x) for x in arg['attributes']])
	elif type(arg) is str:
		return arg				   #already resolved
	else:	
		return arg["variable"]()     #just entity without attributes sent



		

### General ###




def addProp(attribute, value):
	return attribute + ":" + value	
	

def joinList(lis):
	return ', '.join(lis)	

	
def addAttributeToVariable(variable, attribute = ''):
	if(attribute == ''):
		return variable
	elif(attribute.lower() == 'id'):
		return "ID(" + variable + ")"
	else:
		return variable + "." + attribute



def buildVariable(entity, attributes = None): 
	etype = entity['type']()
	variable = entity['variable']()
	label = entity['label']()


	if label != '':
		variable = variable + ":" + label
	if attributes is not None:
		variable = variable + " { "+ addValueToAttribute(entity['attributes'](),attributes) +" }"


	if etype == "Node":
		return "(" + variable + ")"
	else: 
		return "[" + variable + "]"



def addValueToAttribute(validatt, att):
		attstr = ""
		for key, value in att.items():
			if key in validatt:
				attstr += key + ":" + value + ", "
		return attstr[:-2]



