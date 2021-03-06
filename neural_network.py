from pybrain.datasets import SupervisedDataSet
from pybrain.structure.modules import LSTMLayer
from pymongo import MongoClient
import pymongo
import random
import pickle
DS = SupervisedDataSet(11, 1)


class NNTrainer:


	db = MongoClient().test_database
	query = ''
	test = [ 0.0, 0.0, 0.0]
	
	

	def __init__(self, query):
		self.query = query


	def loadData(self):
		i = 0
		prev_count = 0.0
		count = 0
		sentiment = []
		for data in self.db[self.query].find().sort("_id", 1):
			#if i > 30:
			#	break
			if i > 0:
				count = data["count"]
				try:
					DS.addSample(tuple(sentiment), (count),)
				except ValueError:
					continue
			sentiment = data["sentiment"]
			prev_count = data["count"]
			for key in sentiment.keys():
				sentiment[key] = float(float(sentiment[key])/prev_count)
			sentiment = sentiment.values()
			i = i + 1

	def train_output(self):

		from pybrain.tools.shortcuts import buildNetwork
		from pybrain.structure import SigmoidLayer
		FNN = buildNetwork(DS.indim, 20, DS.outdim, bias=True, recurrent=True, hiddenclass=SigmoidLayer)
		from pybrain.supervised.trainers import BackpropTrainer
		TRAINER = BackpropTrainer(FNN, dataset=DS, learningrate = 0.0001, 
		    momentum=0.1, verbose=True)
		for i in range(25000):
			print "Test" + str(i)
			TRAINER.train()
		fileObject = open('neural_network_model.txt', 'w')
		pickle.dump(FNN, fileObject)
		fileObject.close()


a = NNTrainer("nyfw")
a.loadData()
a.train_output()
#fileObject = open('filename','r')
#net = pickle.load(fileObject)
#for data in db.nyfw.find().sort("_id", 1):
#	sentiment = data["sentiment"]
#	count = data["count"]
#	total = total + count
#	for key in sentiment.keys():
#		sentiment[key] = float(float(sentiment[key])/count)
#	sentiment = sentiment.values()
#	print FNN.activate(  test )