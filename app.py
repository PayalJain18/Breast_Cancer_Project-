import streamlit as st
import numpy as np
import pandas as pd
import sklearn.datasets
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# ---------------- Load and Train Model ---------------- #
@st.cache_data
def load_and_train_model():
    # Load dataset
    breast_cancer_dataset = sklearn.datasets.load_breast_cancer()
    df = pd.DataFrame(breast_cancer_dataset.data, columns=breast_cancer_dataset.feature_names)
    df['label'] = breast_cancer_dataset.target

    X = df.drop(columns='label', axis=1)
    Y = df['label']

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
    
    model = LogisticRegression(max_iter=5000)
    model.fit(X_train, Y_train)
    
    return model, breast_cancer_dataset.feature_names

model, feature_names = load_and_train_model()

# ---------------- Streamlit UI ---------------- #
st.set_page_config(page_title="OncoCheck", layout="wide")
st.title("🩺 OncoCheck - Breast Cancer Prediction")
st.write("Enter the tumor features below to predict whether the tumor is **Benign** or **Malignant**.")

# Sidebar for input features
st.sidebar.header("Input Tumor Features")
input_data = []
for feature in feature_names:
    val = st.sidebar.number_input(feature, value=float(np.mean(model.coef_)))
    input_data.append(val)

# Prediction
if st.sidebar.button("Predict"):
    input_array = np.array(input_data).reshape(1, -1)
    prediction = model.predict(input_array)[0]
    result = "Benign" if prediction == 1 else "Malignant"
    
    st.subheader("Prediction Result")
    if result == "Benign":
        st.success(f"✅ Tumor is predicted as **{result}**")
    else:
        st.error(f"❌ Tumor is predicted as **{result}**")
