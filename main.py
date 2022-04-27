from pymongo import MongoClient
from secrets import MONGO_URI, CLIENT_ID, CLIENT_SECRET, USER_AGENT
from datetime import datetime
import pytz
import praw
import logging


client = MongoClient(MONGO_URI)
db = client.get_database("reddit-posts")

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
)


submissions =  reddit.subreddit('btc+eth').stream.submissions()

for submission in submissions:
    j = {k: v for k,v in submission.__dict__.items() if k != '_reddit'}
    j['author'] = j['author'].name
    j['subreddit'] = j['subreddit'].name

    db.get_collection(j["subreddit"]).insert_one(j)