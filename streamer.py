import threading
import tweepy
from datetime import datetime
import re
import keys
from pprint import pprint
from textblob import TextBlob

# Determine whether a tweet is a retweet
get_rt_start_pattern = re.compile(u"(^RT @[^:]+: )")

def is_rt(string):
    return len(get_rt_start_pattern.findall(string)) > 0

def get_status_info(status, keyword):
    document = {
        'text' : status.text if not status.truncated else status.extended_tweet['full_text'],
        'keyword' : keyword
    }

    blob = TextBlob(document['text'])
    document['sentiment'] = blob.sentiment.polarity

    return document if keyword in document['text'] else None

# returns the document for saving
def filter_tweet(status, keyword):
    if is_rt(status.text) or status.lang != 'en':
        return None

    return get_status_info(status, keyword)

class MyStreamListener(tweepy.StreamListener):

    def __init__(self, keyword):
        self.keyword = keyword
        super(MyStreamListener, self).__init__()

    def on_status(self, status):
        tweet = filter_tweet(status, self.keyword)    # will return None if is RT, not in english, or keyword not present in text

        if tweet is not None:
            pprint(tweet)

    def on_error(self, status_code):
        if status_code == 420:          # disconnected by twitter, usually for exceeding rate limits
            print('Connection error in stream', self.keyword)
            return False            # returning False disconnects the stream

class Streamer(threading.Thread):

    def __init__(self, keyword):
        # Twitter authentication
        self.auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
        self.auth.set_access_token(keys.access_token, keys.access_token_secret)
        self.api = tweepy.API(self.auth)
        self.keyword = keyword
        super(Streamer, self).__init__()

    def run(self):
        try:
            self.start_stream()
        except Exception as e:
            if "IncompleteRead" in repr(e):             # common error where the stream is faster than the machine can handle
                print('Incomplete read in', self.keyword)
            else:
                print('Stream', self.keyword, 'stopped. Error:', e)

    # keyword is the desired streaming term
    def start_stream(self):
        self.myStream = tweepy.Stream(auth=self.api.auth, listener=MyStreamListener(self.keyword))
        self.myStream.filter(track=self.keyword)
