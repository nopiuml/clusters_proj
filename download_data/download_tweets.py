from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import time
import json
from pymongo import MongoClient
import json


ckey = 'Okt2tA2dQxoXjxpYjYgZBff40'
csecret = 'hwkatEDjLRwDdSLzuoWYk6MFtwLFLe3DO91yS69nD87wdUrBuS'
atoken = '2790146134-hae3iUDJeURk8S1fWTMQfUzBLQ2IFaIZlPT9VQ0'
asecret = 'rZ3fpd4f74xZqZ4YS3DhWdrr5rPBqdaon0SyYW7lNoHE7'

start_time = time.time() #grabs the system time


class listener(StreamListener):

	def __init__(self, start_time, time_limit):

		self.time = start_time
		self.limit = time_limit

	def on_data(self, data):

		while (time.time() - self.time) < self.limit:

			try:
				client = MongoClient('83.212.109.120', 27017)
# 				db = client['twitter_db']
# 				collection = db['twitter_collection']
				db = client['london_db']
# 				collection = db['wednesday_coll']
				collection = db['thursday_coll']
				tweet = json.loads(data)

				collection.insert(tweet)


				return True


			except BaseException, e:
				print 'failed ondata,', str(e)
				time.sleep(5)
				pass

		exit()
		client.close()

	def on_error(self, status):
		print status



print "start"
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken,asecret)
twitterStream = Stream(auth,listener(start_time, time_limit=3600)) # this is the timeout limit
# twitterStream.filter(track=['San Francisco'],locations=[-122.75,36.8,-121.75,37.8],languages=['en']) #longitude,latitude
twitterStream.filter(locations=[-0.2149200439,51.443308704,-0.041885376,51.5710950133],languages=['en']) #longitude,latitude
