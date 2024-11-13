import requests
from database import store_data_in_db  # Import your database functions
from config import API_URLS, API_KEYS, HEADERS_TEMPLATE  # Import configurations
import time

# Track the index of the API key being used for the specific service
api_key_index = 0

def get_headers(service_key):
    """
    Get headers with the current API key for the specified service.
    Rotates the API key for the given service.
    """
    global api_key_index
    headers = HEADERS_TEMPLATE.copy()
    
    # Retrieve the list of API keys for the specified service
    api_keys = API_KEYS.get(service_key, [])
    if not api_keys:
        raise ValueError(f"No API keys found for service: {service_key}")

    # Use the current API key and rotate to the next one
    headers["x-rapidapi-key"] = api_keys[api_key_index]
    api_key_index = (api_key_index + 1) % len(api_keys)
    return headers

def fetch_and_store_property_list(postal_code, limit=200, offset=0):
    """
    Fetches and stores property data for a given postal code.
    """
    total_fetched = 0
    retries = 3  # Number of retries for handling server errors

    while True:
        payload = {
            "limit": limit,
            "offset": offset,
            "postal_code": str(postal_code),  # Ensure postal code is a string
            "status": ["for_sale", "ready_to_build"],
            "sort": {
                "direction": "desc",
                "field": "list_date"
            }
        }

        headers = get_headers("rapidapi")  # Use API keys for 'rapidapi' service

        # Sending API request
        response = requests.post(API_URLS["property_list"], json=payload, headers=headers)

        # Checking the response
        if response.status_code == 200:
            properties = response.json().get('data', {}).get('home_search', {}).get('results', [])
            if not properties:
                print(f"No properties found for postal code {postal_code}.")
                break  # Exit the loop if no properties are found

            # Store each property in the database
            for property_data in properties:
                property_id = property_data.get('property_id')
                if property_id:
                    store_data_in_db(property_id, property_data)

            total_fetched += len(properties)
            offset += limit  # Update the offset for the next batch

        elif response.status_code == 500:
            if retries > 0:
                retries -= 1
                print(f"Server error for postal code {postal_code}. Retrying in 5 seconds...")
                time.sleep(5)  # Wait before retrying
                continue
            else:
                print(f"Failed to fetch data for postal code {postal_code} after multiple retries.")
                break

        else:
            print(f"Failed to fetch data for postal code {postal_code}. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            break  # Exit on other failures

    return total_fetched

# Dictionary containing counties and their corresponding ZIP codes
'''
zip_codes_dfw = {
    "Dallas County": [
        75001, 75006, 75007, 75019, 75039, 75041, 75042, 75043, 75044, 75048, 
        75050, 75051, 75052, 75060, 75061, 75062, 75080, 75081, 75082, 75088, 
        75089, 75201, 75202, 75203, 75204, 75205, 75206, 75207, 75208, 75209, 
        75210, 75211, 75212, 75214, 75215, 75216, 75217, 75218, 75219, 75220, 
        75221, 75222, 75223, 75224, 75225, 75226, 75227, 75228, 75229, 75230, 
        75231, 75232, 75233, 75234, 75235, 75236, 75237, 75238, 75240, 75241, 
        75242, 75243, 75244, 75246, 75247, 75248, 75249, 75251, 75252, 75253, 
        75254, 75270, 75287, 75301, 75303, 75312, 75315, 75320, 75326, 75336, 
        75339, 75342, 75354, 75355, 75356, 75357, 75358, 75359, 75360, 75367, 
        75368, 75370, 75371, 75372, 75373, 75374, 75376, 75378, 75379, 75380, 
        75381, 75382, 75389, 75390, 75392, 75393, 75394, 75395, 75397, 75398
    ],
    "Tarrant County": [
        76001, 76006, 76008, 76010, 76011, 76012, 76013, 76014, 76015, 76016, 
        76017, 76020, 76021, 76022, 76028, 76034, 76036, 76039, 76040, 76051, 
        76052, 76053, 76054, 76063, 76092, 76101, 76102, 76103, 76104, 76105, 
        76106, 76107, 76108, 76109, 76110, 76111, 76112, 76113, 76114, 76115, 
        76116, 76117, 76118, 76119, 76120, 76121, 76122, 76123, 76124, 76126, 
        76127, 76129, 76130, 76131, 76132, 76133, 76134, 76135, 76136, 76137, 
        76140, 76147, 76148, 76150, 76155, 76161, 76162, 76163, 76164, 76166, 
        76177, 76179, 76180, 76182, 76185, 76190, 76191, 76192, 76193, 76195, 
        76196, 76197, 76198, 76199
    ],
    "Collin County": [
        75002, 75009, 75013, 75023, 75024, 75025, 75034, 75035, 75069, 75070, 
        75071, 75074, 75075, 75078, 75093, 75094, 75098, 75407
    ],

    "Denton County": [
        75007, 75009, 75010, 75019, 75022, 75028, 75034, 75056, 75065, 75068, 
        75077, 76201, 76205, 76207, 76208, 76209, 76210, 76226, 76227, 76247, 
        76249, 76258, 76259, 76262, 76266
    ],
    "Rockwall County": [
        75032, 75087, 75189
    ],
    "Kaufman County": [
        75114, 75126, 75142, 75143, 75147, 75149, 75161, 75182, 75189
    ],
    "Parker County": [
        76008, 76020, 76023, 76035, 76066, 76085, 76086, 76087, 76088
    ],
    "Johnson County": [
        76009, 76028, 76031, 76033, 76044, 76050, 76058, 76059, 76061, 76093
    ]
}

# Loop through each county and its ZIP codes
for county, zip_codes in zip_codes_dfw.items():
    for postal_code in zip_codes:
        total_fetched = fetch_and_store_property_list(postal_code)
        print(f"{county} - ZIP Code {postal_code}: Total properties fetched and stored: {total_fetched}")
'''