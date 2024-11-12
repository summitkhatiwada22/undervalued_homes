import requests
from config import API_KEYS

def fetch_and_store_data(location):
    from database import store_data_in_db  # Import within the function to avoid circular imports
    
    # Example API request (replace with actual API)
    url = f"https://example.com/api/data?location={location}&key={API_KEYS['example_api']}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        store_data_in_db(location, data)
        return data
    else:
        print(f"Failed to fetch data for {location}. Status code: {response.status_code}")
        return None
