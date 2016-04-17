from pybrain.datasets import SupervisedDataSet
from pybrain.structure.modules import LSTMLayer
from pymongo import MongoClient
import pymongo
import random
import pickle

total = 0.0
db = MongoClient().test_database
fileObject = open('neural_network_model.txt','r')
FNN = pickle.load(fileObject)
for data in db.type1diabetes.find().sort("_id", 1):
	sentiment = data["sentiment"]
	count = data["count"]
	total = total + count
	for key in sentiment.keys():
		sentiment[key] = float(float(sentiment[key])/count)
	sentiment = sentiment.values()
	prediction = FNN.activate(  sentiment )
	if prediction < 0:
		prediction = 0.0
	print "Percent. of Accuracy: " + str((prediction - float(count)) / float(count)) + " Prediction: " + str(prediction) + " Actual: " + str(float(count))

fileObject = open('neural_network_model.txt', 'w')

pickle.dump(FNN, fileObject)

fileObject.close()