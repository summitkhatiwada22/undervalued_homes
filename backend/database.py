from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.real_estate_db

# Create an index on the 'location' field (if not already created)
db.properties.create_index('location', unique=True)

def store_data_in_db(location, data):
    """
    Stores or updates data for a given location in the 'properties' collection.
    """
    try:
        collection = db.properties
        collection.update_one({'location': location}, {'$set': {'data': data}}, upsert=True)
        print(f"Data for location '{location}' stored successfully.")
    except Exception as e:
        print(f"Error storing data for location '{location}': {e}")

def get_data_from_db(location):
    """
    Retrieves data for a given location from the 'properties' collection.
    """
    try:
        collection = db.properties
        result = collection.find_one({'location': location})
        return result['data'] if result else None
    except Exception as e:
        print(f"Error retrieving data for location '{location}': {e}")
        return None
