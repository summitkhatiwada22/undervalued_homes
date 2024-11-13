# Test collection existence
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.real_estate_db
print("Collections in real_estate_db:", db.list_collection_names())

# Verify data existence
collection = db.properties
document_count = collection.count_documents({})
print(f"Number of documents in 'properties' collection: {document_count}")

# Optionally, display a sample document
sample_doc = collection.find_one()
print("Sample Document:", sample_doc)
