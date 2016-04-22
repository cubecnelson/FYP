import plotly
import datetime
print plotly.__version__  # version >1.9.4 required
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout
from pymongo import MongoClient
from array import array

# Scientific libraries
import numpy as np

db = MongoClient().test_database
for name in db.collection_names():
	if name == 'nyfw':
		hashtag = name
		count = [];
		date = [];
		xaxis = [];
		i = 0;
		total = 0.0
		totalcount = 0
		#getting the frequency of hashtag
		# stroing in x and y vectors
		for tweet in db[hashtag].find().sort("_id", 1):
			date_datetime = str(tweet["Date"])
			total = tweet["count"]
			totalcount = totalcount + total
			count.append(totalcount)
			date.append(datetime.datetime.strptime(date_datetime,'%Y%m%d').date())
			i = i+ 1

		y = count[:-7]
		x = date[:-7]
		totalnum = -len(x)/2 + 1
		day = []
		for index in range(len(x)):
			xaxis.append(totalnum)
			day.append(index)
			totalnum = totalnum + 1
		
		# calculate polynomial
		z = np.polyfit(xaxis, y, abs(totalnum))
		f = np.poly1d(z)
		
		print f
		
		# calculate new x's and y's
		#calculate by day
		#if totalnum < i/2:
		#	xaxis.append(totalnum)
		#	totalnum = totalnum + 1
			
		y_old = 0
		#print predict.poly(y,totalnum-1)
		x_new = np.linspace(xaxis[0], xaxis[-1]+1, i)
		y_new = f(x_new)
		checking = len(y_new)
		initial = 0
		
		error = 0
		current = 0
		for newy in y_new:
			#print abs((newy - count[current])/count[current])
			error = error + (abs((newy - count[current])/count[current]))
			current = current + 1
		
		while checking > initial:
			print y_new[initial] - y_old
			y_old = y_new[initial]
			initial = initial + 1
		
		print y_new
		print "mean absolute error: " 
		print error/len(x)
		
		x_new = np.linspace(xaxis[0], xaxis[-1]+1, i*10)
		y_new = f(x_new)
		
		
		
		# Creating the dataset, and generating the plot
		trace1 = go.Scatter(
                  x=xaxis, 
                  y=y, 
                  mode='markers',
                  marker=go.Marker(color='rgb(255, 127, 14)'),
                  name='Data'
                  )
		
		#generating the curve that best fit
		trace2 = go.Scatter(
                  x=x_new, 
                  y=y_new, 
                  mode='lines',
                  marker=go.Marker(color='rgb(31, 119, 180)'),
                  name='Fit'
                  )
		
		layout = go.Layout(title=hashtag,
                plot_bgcolor='rgb(229, 229, 229)',
                  xaxis=go.XAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)', range = [date[0],date[-1]]),
                  yaxis=go.YAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)')
				 )
		
		data = [trace1,trace2]
		
		fig = go.Figure(data=data, layout=layout)

		plotly.offline.plot(fig, filename=hashtag+'.html')