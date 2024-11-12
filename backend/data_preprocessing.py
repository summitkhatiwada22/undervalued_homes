import pandas as pd

def preprocess_data(data):
    # Convert data to DataFrame (dummy example for testing)
    df = pd.DataFrame(data if isinstance(data, list) else [data])
    df.fillna(0, inplace=True)  # Example preprocessing step
    return df
