# Marvel vs DC
This project was a test to live streaming, classifying and presenting the live twitter sentiment of some of the most famous heroes from DC and Marvel.

The project works by simultaneosly streaming tweets relative to the heroes chosen, saving the filtered and classified tweets to a local running mongoDB instance, and using MongoDB's aggregation framework to separate the data in time frames and display the results with matplotlib.

To execute, just `git clone` this repository, create a file named `keys.py`, which should contain your twitter API keys in the following format:

```
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
```

Insert the keys between ' '

Run it with:

```
python main.py
```

Dependencies:

- Python 3
- Tweepy
- TextBlob
- Pymongo
- Matplotlib
