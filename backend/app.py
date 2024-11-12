from flask import Flask, request, jsonify, render_template
from data_collection import fetch_and_store_data
from data_preprocessing import preprocess_data
from database import get_data_from_db

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def predict():
    from model import predict_undervalued_properties  # Import within the function to avoid circular imports

    location = request.args.get('location', 'DefaultLocation')
    
    # Fetch data from MongoDB (or from an API if not found in the database)
    data = get_data_from_db(location)
    if not data:
        data = fetch_and_store_data(location)
        if not data:
            return jsonify({"error": "Data could not be retrieved"}), 400

    # Preprocess and predict undervalued properties
    processed_data = preprocess_data(data)
    predictions = predict_undervalued_properties(processed_data)
    
    return jsonify(predictions)

if __name__ == '__main__':
    app.run(debug=True)
