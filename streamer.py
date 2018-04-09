import threading
import tweepy
from datetime import datetime
import re
import keys
from pprint import pprint
from textblob import TextBlob
from pymongo import MongoClient
import pymongo

# Twitter authentication
auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)
api = tweepy.API(auth)

def get_db():
    return MongoClient().threads

def get_text(status):
    if not status.truncated:
        text = status.text
    else:
        text = status.extended_tweet['full_text']

    return text

def get_status_info(status, publisher):
    try:
        if "RT" in status.text:
            text = get_text(status.retweeted_status)
        else:
            text = get_text(status)
    except:
        text = get_text(status)

    document = {
        'text' : text,
        'publisher' : publisher,
        'date' : status.created_at
    }

    blob = TextBlob(document['text'])
    document['sentiment'] = blob.sentiment.polarity

    return document

# returns the document for saving
def filter_tweet(status, publisher):
    if status.lang != 'en':
        return None

    return get_status_info(status, publisher)

class MyStreamListener(tweepy.StreamListener):

    def __init__(self, publisher):
        self.publisher = publisher
        db = get_db()
        if publisher == 'DC':
            self.collection = db.dc
        else:
            self.collection = db.marvel

        super(MyStreamListener, self).__init__()

    def on_status(self, status):
        print("received status in", self.publisher)
        tweet = filter_tweet(status, self.publisher)    # will return None if not in english

        if tweet is not None:
            r = self.collection.insert_one(tweet)
            if not r.acknowledged:
                print("mongo not working")

    def on_error(self, status_code):
        if status_code == 420:          # disconnected by twitter, usually for exceeding rate limits
            print('Connection error in stream', self.publisher)
            return False            # returning False disconnects the stream

# keywords are the desired streaming terms
def start_stream(keywords, publisher):
    myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener(publisher))
    myStream.filter(track=keywords)

class Streamer(threading.Thread):

    def __init__(self, publisher, keywords):
        self.publisher = publisher
        self.keywords = keywords
        super(Streamer, self).__init__()

    def run(self):
        try:
            start_stream(self.keywords, self.publisher)
        except Exception as e:
            if "IncompleteRead" in repr(e):             # common error where the stream is faster than the machine can handle
                print('Incomplete read in', self.publisher)
            else:
                print('Stream', self.publisher, 'stopped. Error:', e)
