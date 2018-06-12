import json

class DataObject(object):
	data = ''
	def __init__(self, dataFunc = None):
			if dataFunc is not None:
				self.data = dataFunc()





