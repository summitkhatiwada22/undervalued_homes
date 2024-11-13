import os
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from pymongo import MongoClient

def create_output_folder(folder_name="processed_data"):
    """
    Creates a folder for storing processed data files if it doesn't already exist.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def scale_and_encode_features(df):
    """
    Scales numerical features and encodes the 'postal_code' feature.
    """
    scaler = StandardScaler()
    # Features to scale
    numerical_features = [
        'description.beds', 'description.baths', 'description.lot_sqft', 
        'description.sqft', 'description.baths_full', 'description.baths_half', 
        'estimate.estimate', 'list_price', 'price_per_sqft', 
        'lot_to_building_ratio', 'bathrooms_per_bedroom', 'total_rooms', 
        'price_to_estimate_ratio', 'neighborhood_median_price', 
        'relative_price_difference_to_estimate'
    ]
    df[numerical_features] = scaler.fit_transform(df[numerical_features])

    # One-hot encode postal code
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')  # Corrected parameter
    encoded_postal_code = encoder.fit_transform(df[['location.address.postal_code']])
    postal_code_df = pd.DataFrame(encoded_postal_code, columns=encoder.get_feature_names_out())

    # Drop original postal code column and concatenate encoded data
    df = df.drop('location.address.postal_code', axis=1)
    df = pd.concat([df, postal_code_df], axis=1)

    return df


def preprocess_data(data):
    """
    Preprocesses the input data by extracting relevant fields, creating features, 
    handling missing values, scaling features, and saving the cleaned DataFrame.
    """
    extracted_data = []
    for record in data:
        location = record.get('location') or {}
        address = location.get('address') or {}

        # Property type encoding
        property_type = record.get('description', {}).get('type', 'Unknown')
        is_single_family = 1 if property_type == 'single_family' else 0
        is_townhome = 1 if property_type == 'townhome' else 0
        is_condo = 1 if property_type == 'condo' else 0

        # Feature calculations with None handling
        sqft = record.get('description', {}).get('sqft') or 0
        lot_sqft = record.get('description', {}).get('lot_sqft') or 0
        list_price = record.get('list_price') or 0
        estimate = record.get('estimate')
        estimate_value = estimate.get('estimate', 0) if estimate else 0
        beds = record.get('description', {}).get('beds') or 0
        baths = record.get('description', {}).get('baths') or 0

        price_per_sqft = list_price / max(sqft, 1)  # Avoid division by zero
        lot_to_building_ratio = lot_sqft / max(sqft, 1)  # Avoid division by zero
        bathrooms_per_bedroom = baths / max(beds, 1)  # Avoid division by zero
        total_rooms = beds + baths
        price_to_estimate_ratio = list_price / max(estimate_value, 1)  # Avoid division by zero

        extracted_record = {
            'is_single_family': is_single_family,
            'is_townhomes': is_townhome,
            'is_condos': is_condo,
            'description.beds': beds,
            'description.baths': baths,
            'description.lot_sqft': lot_sqft,
            'description.sqft': sqft,
            'description.baths_full': record.get('description', {}).get('baths_full') or 0,
            'description.baths_half': record.get('description', {}).get('baths_half') or 0,
            'estimate.estimate': estimate_value,
            'list_price': list_price,
            'price_per_sqft': price_per_sqft,
            'lot_to_building_ratio': lot_to_building_ratio,
            'bathrooms_per_bedroom': bathrooms_per_bedroom,
            'total_rooms': total_rooms,
            'price_to_estimate_ratio': price_to_estimate_ratio,
            'location.address.postal_code': address.get('postal_code', '00000'),
            'neighborhood_median_price': 0,  # Placeholder, calculated later
            'relative_price_difference_to_estimate': 0  # Placeholder, calculated later
        }
        extracted_data.append(extracted_record)

    # Convert to DataFrame
    df = pd.DataFrame(extracted_data)

    # Calculate neighborhood median price by postal code
    median_price_by_postal_code = df.groupby('location.address.postal_code')['list_price'].median().to_dict()
    df['neighborhood_median_price'] = df['location.address.postal_code'].map(median_price_by_postal_code)

    # Calculate relative price difference to the estimated price
    df['relative_price_difference_to_estimate'] = (df['list_price'] - df['estimate.estimate']) / max(df['estimate.estimate'].max(), 1)

    # Scale and encode features
    df = scale_and_encode_features(df)

    # Save DataFrame as CSV in the output folder
    output_folder = create_output_folder()
    output_path = os.path.join(output_folder, 'training_features.csv')
    df.to_csv(output_path, index=False)
    print(f"Feature DataFrame saved as '{output_path}'")
    print("Sample DataFrame:")
    print(df.head())  # Display the first few rows

    return df

if __name__ == "__main__":
    # from database import get_data_from_db  # Assuming you have this function to fetch data

    # Connect to MongoDB and fetch all data from the collection
    client = MongoClient('mongodb://localhost:27017')  # Replace with your actual URI if different
    db = client.real_estate_db
    collection = db.properties

    # Fetch all data from the MongoDB collection
    data = list(collection.find())  # This fetches all data; modify if needed for testing

    # Preprocess and save data
    df = preprocess_data(data)
    print(f"Total number of records processed: {len(df)}")
