from pymongo import MongoClient
from config import MONGO_URL

client = MongoClient(MONGO_URL)
db = client.real_estate_db
collection = db.properties  # Use a reference for the collection

# Create an index on the 'property_id' field (unique identifier)
collection.create_index('property_id', unique=True)

def store_data_in_db(property_id, data):
    """
    Stores or updates data for a given property_id in the 'properties' collection.
    """
    try:
        collection.update_one(
            {'property_id': property_id},  # Use property_id as the unique identifier
            {'$set': data},
            upsert=True  # Insert if not exists, otherwise update
        )
    except Exception as e:
        print(f"Error storing data for property_id '{property_id}': {e}")

def get_data_from_db(property_id):
    """
    Retrieves data for a given property_id from the 'properties' collection.
    """
    try:
        result = collection.find_one({'property_id': property_id})
        return result if result else None
    except Exception as e:
        print(f"Error retrieving data for property_id '{property_id}': {e}")
        return None
