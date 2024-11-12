from sklearn.linear_model import LinearRegression
import pandas as pd

def train_model(data):
    if isinstance(data, pd.DataFrame) and not data.empty:
        X = data.iloc[:, :-1]  # Assuming all columns except the last are features
        y = data.iloc[:, -1]   # Assuming the last column is the target
        model = LinearRegression()
        model.fit(X, y)
        return model
    return None

def predict_undervalued_properties(data):
    model = train_model(data)
    if model:
        predictions = model.predict(data.iloc[:, :-1])
        return predictions.tolist()
    return []
