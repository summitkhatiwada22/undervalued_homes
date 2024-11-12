from database import store_data_in_db, get_data_from_db

# Test data for storing
test_location = "Test Location"
test_data = {
    "name": "Sample Property",
    "price": 200000,
    "size": 1200,
    "type": "Apartment"
}

# Test storing data
print("Storing data...")
store_data_in_db(test_location, test_data)

# Test retrieving data
print("Retrieving data...")
retrieved_data = get_data_from_db(test_location)
if retrieved_data:
    print(f"Data retrieved for location '{test_location}': {retrieved_data}")
else:
    print(f"No data found for location '{test_location}'.")
