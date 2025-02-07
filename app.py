from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import sklearn.datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from flask_cors import CORS

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

# API Endpoint for Predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from frontend
        data = request.json['input_data']
        input_data_np = np.asarray(data).reshape(1, -1)  # Convert to NumPy array
        prediction = model.predict(input_data_np)[0]  # Get prediction

        return jsonify({'prediction': int(prediction)})  # Return response as JSON
    except Exception as e:
        return jsonify({'error': str(e)})  # Handle errors gracefully

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)