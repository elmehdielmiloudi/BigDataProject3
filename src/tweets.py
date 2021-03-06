from url_finder import *
import pandas as pd
import numpy as np
from time import *
'''
In this module, we process tweets, iterate and extract data from them.
'''
def has_tweets(userID,tweetsDF):
	return tweetsDF[tweetsDF['user_id'] == userID].empty

def get_tweets_count(userID,tweetsDF):
	'''
	This will count the number of tweets done by a
	'''
	userTweets = get_tweets_user(userID,tweetsDF)

	return len(userTweets)

def get_tweets_user(userID,tweetsDF):
	'''
	This function returns the list of tweets belonging to a particular userID
	'''
	return tweetsDF['text'][tweetsDF['user_id']== userID].tolist()

def get_tweets_dataframe_user(userID,tweetsDF):
	'''
	This function returns the tweets belonging to a particular userID
	'''
	#t0 = time()
	user_id = tweetsDF['user_id'] == userID
	res = tweetsDF[user_id]
	#print ("tweet user:", round(time()-t0, 3), "s")
	return res

def count_user_tweets(userID, tweetsDF):
	return len(get_tweets_user(userID,tweetsDF))


def get_avg_friends_tweets(friendsIDlist,tweetsDF):
	friends_count 		= len(friendsIDlist)
	total_tweet_count 	= 0
	friendsIDlist = pd.Series(friendsIDlist)

	total_tweet_count = tweetsDF[tweetsDF['user_id'].isin(friendsIDlist)].shape[0]
	if friends_count == 0:
		friends_count = 0.001
	return total_tweet_count/friends_count



def get_tweets_strings(userID,tweetsDF):
	'''
	Searches for a user's tweets and saves all the text from
	the tweets in 1 string
	'''

	tweets_user = get_tweets_dataframe_user(userID,tweetsDF)
	res = tweets_user['text'].str.cat()
	return res


def get_tweets_with_url_ratio(userID, tweetsDF):
	t0 = time()
	#print("ID ----"+str(userID))
	#print(tweetsDF.head())
	user_tweets = tweetsDF['user_id'] == userID
	#urlTweets 	= tweetsDF[user_tweets &(tweetsDF['text'].apply(lambda tweet: tweet_contains_url(tweet)))]
	urlTweets 	= tweetsDF[user_tweets & tweetsDF['text']]
	new_value = urlTweets['text'].apply(lambda tweet: tweet_contains_url(tweet))
	#print(new_value)
	#print("TEST:", round(time()-t0, 3), "s")
	tweets_with_url 	= new_value.mean()
	#print("tweets_with_url: "+str(tweets_with_url))
	user_tweets_count 	= count_user_tweets(userID,tweetsDF)
	if(user_tweets_count == 0):
		user_tweets_count = 0.001
		
	return float(tweets_with_url)/float(user_tweets_count)


def tweet_contains_url(tweet):
	return has_url(tweet)

def get_api_tweets_count(userTweetsDF):
	'''
	The tweetDF only contains tweets from a single user
	'''
	tweets = userTweetsDF[userTweetsDF['text'].apply(lambda tweet : tweet.count("API")>0)]

	return len(tweets.tolist())

def retweet_ratio(userID, tweetsDF):
	tweets = tweetsDF[tweetsDF['user_id'] == userID]

	tweetsCount = tweets.shape[0]

	retweets = tweets[tweets['retweet_count']>0].shape[0]

	if(tweetsCount == 0):
		#print("-----------------Retweet 0")
		return 0

	else:
		res = retweets/tweetsCount
		#print("-----------------Retweet : "+str(res))
		return res