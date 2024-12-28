from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle

app = Flask(__name__)

# Load your dataset
data = pd.read_csv('C:\\Users\\ajju1\\PycharmProjects\\PythonProject\\templates\\auto-mpg.csv')


data['horsepower'] = pd.to_numeric(data['horsepower'], errors='coerce')
data = data.dropna()

X = data[['cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model year', 'origin']]
y = data['mpg']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Save the model
with open('model.pkl', 'wb') as file:
    pickle.dump(rf_model, file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        if not data or 'features' not in data:
            return jsonify({'error': 'No features provided in the request.'}), 400

        features = data['features']

        if not isinstance(features, list) or len(features) != 7:
            return jsonify({'error': 'Features should be a list of 7 numbers.'}), 400

        features = np.array(features).reshape(1, -1)

        # Load the model
        model = pickle.load(open('model.pkl', 'rb'))

        # Make prediction
        prediction = model.predict(features)

        # Convert MPG to km/L
        km_per_l = prediction[0] * 0.425144

        return jsonify({'prediction_mpg': round(prediction[0], 2), 'prediction_km_per_l': round(km_per_l, 2)})

    except Exception as e:
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
