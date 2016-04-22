from pybrain.datasets import SupervisedDataSet
from pybrain.structure.modules import LSTMLayer
from pymongo import MongoClient
import pymongo
import random
import pickle


class NNActivator:
	
	db = MongoClient().test_database

	def __init__ (self,query):
		self.query = query

	def activate(self):
		actual = []
		result = []
		total = 0.0
		error = 0.0
		n = 0
		fileObject = open('neural_network_model.txt','r')
		FNN = pickle.load(fileObject)
		for data in self.db[self.query].find().sort("_id", 1):
			if data["count"] > 0:
				sentiment = data["sentiment"]
				count = data["count"]
				actual.append(count)
				total = total + count
				for key in sentiment.keys():
					sentiment[key] = float(float(sentiment[key])/count)
				sentiment = sentiment.values()
				prediction = FNN.activate(  sentiment )
				if prediction < 0:
					prediction = 0.0
				result.append(float(prediction))
				n = n + 1
		print "Error: " + str(error/n)
		fileObject = open('neural_network_model.txt', 'w')

		pickle.dump(FNN, fileObject)

		fileObject.close()
		result.pop()
		actual.pop(0)
		print result
		print actual

		for i in range(0, len(result)):
			if actual[i] > 20:
				error = error + abs(result[i] - actual[i])/actual[i]

		

		print error/len(result)
a = NNActivator('nyfw')
a.activate()