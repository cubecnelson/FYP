import tweepy
import time
import re
from trend import Trend
import json

consumer_key = "GLc0pEAaojsnM5Kqg769QvbsD"
consumer_secret = "u2opeydedKyKc8mJcw9oQpwvgevKJdSLmSWKHh1hud0Ns9rceX"

access_token = "3241851673-19FXOYEXa0wjoRGOfMK8gxo8lcnCYpKII3C05FB"
access_token_secret = "5hS3zYdV9Z122uQBfHVFlmbq8T3NUxiOdjdyBh4m0vsCU"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

trends = api.trends_place(id='23424977')

trends = trends[0]

trends = trends['trends']

f = open("trend_retweets.txt", "w")



for trend in trends:
	print ('Trends: ',trend['name'], '\n')
	
	tweets = api.search(q=trend['name'], lang='en', count=200, geocode='40.7142700,-74.0059700,15.8476023485km')
	n = 1
	sum = 0	
	first = Trend()
	first.setName(trend['name'])
	for tweet in tweets:
		print ('Tweet ', n, ':', tweet.text.encode("utf-8"))
		for tags in tweet.entities.get('hashtags'):
			print(tags['text'].encode("utf-8").lower())
			first.addToRelated(tags['text'].encode("utf-8").lower(),tweet.retweet_count+1)
		n = n + 1
		sum = sum + tweet.retweet_count + 1
	print ("Retweet Count:",str(sum),'\n')
	f.write(trend['name']+"\t"+str(sum)+'\n\t'+"\n\t".join('{}\t{}'.format(key, val) for key, val in first._related.items())+'\n')
	first.clear()
	