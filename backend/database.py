from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.real_estate_db

def store_data_in_db(location, data):
    collection = db.properties
    collection.update_one({'location': location}, {'$set': {'data': data}}, upsert=True)

def get_data_from_db(location):
    collection = db.properties
    result = collection.find_one({'location': location})
    return result['data'] if result else None
