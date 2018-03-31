import tweepy
from datetime import datetime
import re
import keys
from pprint import pprint

get_rt_start_pattern = re.compile(u"(^RT @[^:]+: )")

def is_rt(string):
    return len(get_rt_start_pattern.findall(string)) > 0

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        tweet = filter_tweet(status)    # will return None if is RT\

        if (tweet is not None) and (tweet['lang'] == 'en'):
            pass
            # process tweet

    def on_error(self, status_code):
        if status_code == 420:
            print('Connection error')
            return False            # returning False disconnects the stream

def get_user_basics(user):
    document = {
        'id' : user.id_str,
        'user_name' : '@' + user.screen_name,
        'name' : user.name,
        'location' : user.location,
        'followers_count' : user.followers_count,
        'following' : user.friends_count,
        'verified' : user.verified,
        'created_at' : user.created_at
    }

    return document

def get_status_info(status):
    document = {
        'id' : status.id_str,
        'user' : get_user_basics(status.user),
        'is_reply' : status.in_reply_to_status_id is not None,
        'in_reply_to_status_id' : status.in_reply_to_status_id_str,
        'retweets' : status.retweet_count,
        'favorites' : status.favorite_count,
        'replies' : status.reply_count,
        'date' : status.created_at,
        'text' : status.text if not status.truncated else status.extended_tweet['full_text'],
        'lang' : status.lang
    }

    return document

# returns the document for saving
def filter_tweet(status):
    if is_rt(status.text):
        return None

    return get_status_info(status)

# keywords must be a string array
def start_stream(keywords):
    print('Starting stream')
    myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
    myStream.filter(track=keywords)

# access keys for Twitter
consumer_key = keys.consumer_key
consumer_secret = keys.consumer_secret
access_token = keys.access_token
access_token_secret = keys.access_token_secret

# Twitter authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
