import plotly
print plotly.__version__  # version >1.9.4 required
from plotly.graph_objs import Scatter, Layout
from pymongo import MongoClient
from array import array

db = MongoClient().test
for name in db.collection_names():
	hashtag = name
	count = [];
	date = [];
	i = 0;
	for tweet in db[hashtag].find():
		count.append(tweet["count"])
		date.append(tweet["Date"])
		i = i+ 1
	print count[:]
	print date[:]
	
	plotly.offline.plot({
	"data": [
		Scatter(x=date, y=count)
	],
	"layout": Layout(
		title=hashtag
	)
	})
