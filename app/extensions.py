from flask_pymongo import PyMongo, MongoClient

client = MongoClient('mongodb://service-mongodb:27017/', username='admin', password='password')
db = client.smartDevApiService