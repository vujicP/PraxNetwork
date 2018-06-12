from neo4j.v1 import GraphDatabase
from neo4j.v1.types import Record, Node, Relationship
import json
import string
from .cypher_query_builder import *
from django.conf import settings



uri = settings.NEO4J_DATABASE_URL
driver = GraphDatabase.driver(uri, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD))



### Processing Action to DB ###


def dbProcessRequest(query):

	# print("      ################## Query #####################")
	# print(query)
	# print("      ################ Query End ###################")
	with driver.session() as session:
		results = session.run(query, None)
		return results


def prepareResponse(results):
	json_formatted_list = toJson(results)
	json_string = json.dumps(json_formatted_list)

	# print("      ################# Results ####################")
	# print(json_string)
	# print("      ############## Results End ###################")
	return json_string
	


def toJson(results):
	json_results = []
	for record in results:
		json_results.append({"record": resolveDict(record,results.keys())})
	return json_results



def resolveDict(line, keys):
		dic = {}
		for key in keys:
			entry = line[key]

			if key.startswith("ID("):
				dic[key[3:-1]] = { "id": entry}      #bring ID return value to better readable format
				if len(keys) == 1:
					dic[key] = resolveEntry(entry)	 #if len(keys) is 1 leave ID() key for extractValues method
			else:
				dic[key] = resolveEntry(entry)

		return dic


def resolveList(arglist):
	retlist = []
	for entry in arglist:
		retlist.append(resolveEntry(entry))
	return retlist


def resolveEntry(entry):
			if isinstance(entry, Node):
				return {"id": entry.id,"labels": json.dumps(list(entry.labels)), "properties": entry.properties} 
			elif isinstance(entry, Relationship):
				return {"id": entry.id, "start": entry.start, "end": entry.end, "type": entry.type, "properties": entry.properties}
			elif isinstance(entry, list):
				return resolveList(entry)
			else: 
				return entry


def processAction(statements):
	@getResponse
	def buildQuery():
		query_parts = statements()
		return " ".join(query_parts) #assumes statements already have cypher-like ordering, tdo: introduce more abstraction
	return buildQuery	



def getResponse(query):
	def get():
		return prepareResponse(dbProcessRequest(query()))
	return get	


def extractValues(response):
	def extract():
		result = json.loads(response())
		if len(result) == 0:
			return result

		record = result[0]['record']

		if len(result) == 1 and len(record.values()) == 1:
			return list(record.values())[0]

		if len(result) == 1 and any(key.startswith("ID(") for key in record):
				for key in record.keys():
					if key.startswith("ID("):
						return record[key]

		if len(result) == 1:
			return result[0]

		return json.dumps(result)
	return extract



###  Statement Identifiers  ###


def generic_action(*args):
	@extractValues
	@processAction
	def statements():
		return args
	return statements



#match variables as path
@buildPath
def match():
	return "MATCH "

@buildPath
def merge():
	return "MERGE "

#match indepedent variables
@buildVarList
def match_indepedent():
	return "MATCH "

@updateValues
def update():
	return "SET {0}"




@buildVariablesToProcess
def ret():
	return "RETURN {0}"

@buildVariablesToProcess
def delete():
	return "DELETE {0}"

@buildVariablesToProcess
def forceDelete():
	return "DETACH DELETE {0}"

@setCollectVariable
@buildVariablesToProcess
def collect():
	return "collect([{0}])"





@equal
@buildWhereClause
def where():
	return "WHERE "

@notEqual
@buildWhereClause
def exclude():
	return ""

@search
@buildWhereClause
def search():
	return ""



