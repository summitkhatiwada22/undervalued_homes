# config.py

# MongoDB Configuration
MONGO_URL = "mongodb://localhost:27017/"  # Replace with your MongoDB connection string

# API Configuration
API_URLS = {
    "property_list": "https://realty-in-us.p.rapidapi.com/properties/v3/list",
    "property_detail": "https://realty-in-us.p.rapidapi.com/properties/v3/detail"  # Example URL for another endpoint
}
API_KEYS = {
    "rapidapi": [
        "87f83c9c02mshe02f88a9e3dd6f7p192b12jsn42029d9b1c76"
    ]
}
HEADERS_TEMPLATE = {
    "x-rapidapi-host": "realty-in-us.p.rapidapi.com",
    "Content-Type": "application/json"
}
