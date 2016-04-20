from pybrain.datasets import SupervisedDataSet
from pybrain.structure.modules import LSTMLayer
from pymongo import MongoClient
import pymongo
import random
import pickle

total = 0.0
error = 0.0
n = 0
db = MongoClient().test_database
fileObject = open('neural_network_model.txt','r')
FNN = pickle.load(fileObject)
for data in db.nyfw.find().sort("_id", 1):
	if data["count"] > 0:
		sentiment = data["sentiment"]
		count = data["count"]
		total = total + count
		for key in sentiment.keys():
			sentiment[key] = float(float(sentiment[key])/count)
		sentiment = sentiment.values()
		prediction = FNN.activate(  sentiment )
		if prediction < 0:
			prediction = 0.0
		print data["_id"] + "\t" + str(prediction[0]) + "\t" + str(float(count)) + "\t" + str(data["sentiment"].values())
		n = n + 1

print "Error: " + str(error/n)
fileObject = open('neural_network_model.txt', 'w')

pickle.dump(FNN, fileObject)

fileObject.close()