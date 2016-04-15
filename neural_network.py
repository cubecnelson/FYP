from pybrain.datasets import SupervisedDataSet
from pybrain.structure.modules import LSTMLayer
from pymongo import MongoClient
import pymongo
import random
import pickle
DS = SupervisedDataSet(11, 1)

db = MongoClient().test_database

count = 0
test = [ ]
i = 0
total = 0
for data in db.nyfw.find().sort("_id", 1):
	sentiment = data["sentiment"]
	count = data["count"]
	total = total + count
	for key in sentiment.keys():
		sentiment[key] = float(float(sentiment[key])/count)

	sentiment = sentiment.values()
	try:
		DS.addSample(tuple(sentiment), (count),)
	except ValueError:
		continue
	
	i = i + 1



from pybrain.tools.shortcuts import buildNetwork
FNN = buildNetwork(DS.indim, 20, DS.outdim, bias=True, hiddenclass=LSTMLayer, recurrent=True)

from pybrain.supervised.trainers import BackpropTrainer
TRAINER = BackpropTrainer(FNN, dataset=DS, learningrate = 0.0001, 
    momentum=0.1, verbose=True)

for i in range(15000):
    TRAINER.train()


fileObject = open('neural_network_model.txt', 'w')

pickle.dump(FNN, fileObject)

fileObject.close()

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