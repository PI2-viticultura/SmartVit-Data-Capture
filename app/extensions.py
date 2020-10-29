from flask_pymongo import MongoClient
from settings import load_database_params
import pymongo
import os

password = os.getenv("MONGOPASSWORD")
dbname = os.getenv("DBNAME", "smart-dev")
env = os.getenv("ENVIRONMENT")

if password and dbname:
    client = MongoClient(
        "mongodb+srv://smartAdmin:"
        + password + "@smartvit.6s6r9.mongodb.net/"
        + dbname + "?retryWrites=true&w=majority"
    )

else:
    client = pymongo.MongoClient(
        **load_database_params(), serverSelectionTimeoutMS=10
    )
