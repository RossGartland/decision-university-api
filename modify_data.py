from pymongo import MongoClient
import random
import uuid
import datetime
from bson import ObjectId

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.com661
events = db.university

for event in events.find():
    events.update_many(
        {"_id": event['_id']},
        {
            "$set": {
                "comments": [{
                    "_id": ObjectId(),
                    "username": "JohnCoffeeLover",
                    "text": "Interesting. Thanks.",
                    "sentDateTime": datetime.datetime.utcnow(),
                    "uptdTimestamp": None,
                    "likeReactions": [],
                    "laughReactions": [],
                    "angryReactions": [],
                    "user_id": "63654f75f0b1692c26035e16",
                }]  # Add comment field to the dataset.
            }
        }
    )
