from flask_pymongo import MongoClient

client = MongoClient(
    'mongodb://data-capture-mongodb:27017/',
    username='admin',
    password='password'
)

db = client.smartDevApiService
