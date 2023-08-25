import pymongo
from pymongo import MongoClient

mongo_uri = ""
connect = MongoClient(mongo_uri)

db = connect["arcane"]
users = db["users"]

user1 = {"id": 0, "email": "emma@gmail.com", "name": "Emma Powell"}
users.insert_one(user1)
