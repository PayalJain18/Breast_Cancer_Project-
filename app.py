from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import sklearn.datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend communication

# Load the breast cancer dataset
breast_cancer_dataset = sklearn.datasets.load_breast_cancer()

# Create a DataFrame
data_frame = pd.DataFrame(breast_cancer_dataset.data, columns=breast_cancer_dataset.feature_names)
data_frame['label'] = breast_cancer_dataset.target  # Add target column

# Split features and target
X = data_frame.drop(columns='label', axis=1)
Y = data_frame['label']

# Train-test split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

# Train Logistic Regression model
model = LogisticRegression(max_iter=5000)
model.fit(X_train, Y_train)

# ---------------- Routes ---------------- #

# Base route (to check app is running)
@app.route('/')
def home():
    return "✅ Breast Cancer Prediction API is live!"

# API Endpoint for Predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from frontend
        data = request.json['input_data']

        # Convert input to NumPy array
        input_data_np = np.asarray(data).reshape(1, -1)

        # Predict
        prediction = model.predict(input_data_np)[0]

        # Map prediction to label
        result = "Benign" if prediction == 1 else "Malignant"

        return jsonify({
            'prediction': int(prediction),
            'result': result
        })

    except Exception as e:
        return jsonify({'error': str(e)})

# Run Flask app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Railway provides PORT env variable
    app.run(host='0.0.0.0', port=port)
