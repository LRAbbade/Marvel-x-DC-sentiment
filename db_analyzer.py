import time
import threading
from datetime import datetime
from pymongo import MongoClient
import pymongo
import matplotlib.pyplot as plt

def get_db():
    return MongoClient().threads

class Analyzer():

    def __init__(self):
        self.db = get_db()
        self.numOfBuckets = 1
        self.marvel = []
        self.dc = []
        super(Analyzer, self).__init__()

    def update_buckets(self):
        self.numOfBuckets += 1

        bucketing = {
            "$bucketAuto" : {
                "groupBy" : "$date",
                "buckets" : self.numOfBuckets,
                "output" : {
                    "sentiment" : { "$avg": "$sentiment" }
                }
            }
        }

        pipeline = [bucketing]
        r_marvel = self.db.marvel.aggregate(pipeline)
        r_dc = self.db.dc.aggregate(pipeline)

        self.marvel = [i['sentiment'] for i in r_marvel]
        self.dc = [i['sentiment'] for i in r_dc]

    def data_listener(self):
        while True:
            time.sleep(1)                  # graph refreshes every 10 seconds
            self.update_buckets()

    def set_plot(self, title):
        axes = plt.gca()
        axes.set_ylim([-1, 1])
        plt.grid(True)
        plt.title(title)

    def start(self):
        self.thread = threading.Thread(target=self.data_listener)
        self.thread.daemon = True
        self.thread.start()

        # initialize figure
        plt.figure()
        ln, = plt.plot([])
        plt.ion()
        plt.show()
        while True:
            plt.pause(1)

            plt.subplot(221)
            plt.plot(self.dc)
            self.set_plot('DC sentiment')

            plt.subplot(222)
            plt.plot(self.marvel)
            self.set_plot('Marvel sentiment')

            plt.tight_layout()
            plt.draw()
