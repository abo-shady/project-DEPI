import pickle
import streamlit as st
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
model_path = BASE_DIR / "best_model.pkl"


try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    print("Model loaded successfully.")

  
    
    st.set_page_config(page_title="Customer Churn Predictor", layout="wide")
    st.title(" Customer Churn Prediction")
    st.write("This app predicts whether a customer is likely to churn based on their details. Please fill in the information on the left sidebar.")

    st.sidebar.header("Enter Customer Details:")

    def get_user_input():
        """Collects and returns user input from the sidebar."""
        #numeric inputs
        age = st.sidebar.number_input("Age", min_value=18, max_value=100, value=30, step=1)
        dependents = st.sidebar.number_input("Number of Dependents", min_value=0, max_value=20, value=0, step=1)
        monthly_charge = st.sidebar.number_input("Monthly Charge ($)", min_value=0.0, value=70.0, format="%.2f")
        total_charges = st.sidebar.number_input("Total Charges ($)", min_value=0.0, value=1000.0, format="%.2f")
        #categorical inputs
        gender = st.sidebar.selectbox("Gender", ("Male", "Female"))
        married = st.sidebar.selectbox("Married", ("Yes", "No"))
        phone_service = st.sidebar.selectbox("Has Phone Service", ("Yes", "No"))
        multiple_lines = st.sidebar.selectbox("Has Multiple Lines", ("Yes", "No", "No phone service"))
        online_security = st.sidebar.selectbox("Has Online Security", ("Yes", "No", "No internet service"))
        online_backup = st.sidebar.selectbox("Has Online Backup", ("Yes", "No", "No internet service"))
        device_protection = st.sidebar.selectbox("Has Device Protection", ("Yes", "No", "No internet service"))
        tech_support = st.sidebar.selectbox("Has Premium Tech Support", ("Yes", "No", "No internet service"))
        streaming_tv = st.sidebar.selectbox("Streams TV", ("Yes", "No", "No internet service"))
        streaming_movies = st.sidebar.selectbox("Streams Movies", ("Yes", "No", "No internet service"))
        paperless_billing = st.sidebar.selectbox("Uses Paperless Billing", ("Yes", "No"))
        internet_type = st.sidebar.selectbox("Internet Type", ("Fiber Optic", "DSL", "No Internet Service"))
        contract = st.sidebar.selectbox("Contract Type", ("Month-to-Month", "One Year", "Two Year"))
        payment_method = st.sidebar.selectbox("Payment Method", ("Credit Card", "Bank Withdrawal", "Mailed Check", "Electronic Check"))
        
        user_data = {
            'age': age,
            'dependents': dependents,
            'monthly_charge': monthly_charge,
            'total_charges': total_charges,
            'gender': gender,
            'married': married,
            'phone_service': phone_service,
            'multiple_lines': multiple_lines,
            'online_security': online_security,
            'online_backup': online_backup,
            'device_protection': device_protection,
            'tech_support': tech_support,
            'streaming_tv': streaming_tv,
            'streaming_movies': streaming_movies,
            'paperless_billing': paperless_billing,
            'internet_type': internet_type,
            'contract': contract,
            'payment_method': payment_method
        }
        return user_data

    user_input = get_user_input()

    if st.sidebar.button("Predict Churn"):
        if model is not None:
            gender_encoded = 1 if user_input['gender'] == 'Male' else 0
            married_encoded = 1 if user_input['married'] == 'Yes' else 0
            phone_service_encoded = 1 if user_input['phone_service'] == 'Yes' else 0
            multiple_lines_encoded = 1 if user_input['multiple_lines'] == 'Yes' else 0
            online_security_encoded = 1 if user_input['online_security'] == 'Yes' else 0
            online_backup_encoded = 1 if user_input['online_backup'] == 'Yes' else 0
            device_protection_encoded = 1 if user_input['device_protection'] == 'Yes' else 0
            tech_support_encoded = 1 if user_input['tech_support'] == 'Yes' else 0
            streaming_tv_encoded = 1 if user_input['streaming_tv'] == 'Yes' else 0
            streaming_movies_encoded = 1 if user_input['streaming_movies'] == 'Yes' else 0
            paperless_billing_encoded = 1 if user_input['paperless_billing'] == 'Yes' else 0
            internet_service_encoded = {'Fiber Optic': 2, 'DSL': 1}.get(user_input['internet_type'], 0)
            contract_encoded = {'Two Year': 2, 'One Year': 1}.get(user_input['contract'], 0)
            payment_method_encoded = {'Credit Card': 1, 'Bank Withdrawal': 2, 'Mailed Check': 3, 'Electronic Check': 4}[user_input['payment_method']]

        features = [
            user_input['age'],
            user_input['dependents'],
            user_input['monthly_charge'],
            user_input['total_charges'],
            gender_encoded,
            married_encoded,
            phone_service_encoded,
            multiple_lines_encoded,
            online_security_encoded,
            online_backup_encoded,
            device_protection_encoded,
            tech_support_encoded,
            streaming_tv_encoded,
            streaming_movies_encoded,
            paperless_billing_encoded,
            internet_service_encoded,
            contract_encoded,
            payment_method_encoded
        ]
        
        final_features = np.array(features).reshape(1, -1) # reshape the input for prediction
        
        prediction = model.predict(final_features)
        prediction_proba = model.predict_proba(final_features)
        
        st.subheader("Prediction Result")
        churn_probability = prediction_proba[0][1] * 100
        
        if prediction[0] == 1:
            st.error(f" This customer is likely to **Churn** (Probability: {churn_probability:.2f}%)")
        else:
            st.success(f" This customer is likely to **Stay** (Probability of Churning: {churn_probability:.2f}%)")

        

    else:
        st.info("Please enter customer details on the left and click 'Predict Churn'.")
    




except FileNotFoundError:
    print(f"Error: Model file not found at {model_path}")
    raise