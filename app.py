"""Streamlit web app.   Run:  streamlit run app.py"""
import streamlit as st
from datetime import datetime
from src.predict import predict_price

st.set_page_config(page_title="Car Price Predictor", page_icon="🚗")
st.title("🚗 Used Car Price Predictor")
st.caption("Enter the car details to get an estimated resale price.")

BRANDS = ["Maruti", "Hyundai", "Honda", "Toyota", "Tata", "Mahindra", "Ford",
          "Volkswagen", "BMW", "Mercedes-Benz", "Audi", "Renault", "Skoda", "Kia"]

c1, c2 = st.columns(2)
brand = c1.selectbox("Brand", BRANDS)
model_name = c2.text_input("Model", "Swift")
year = c1.slider("Manufacturing year", 2000, datetime.now().year, 2018)
km = c2.number_input("Kilometres driven", 0, 500_000, 40_000, step=1_000)
fuel = c1.selectbox("Fuel", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
transmission = c2.selectbox("Transmission", ["Manual", "Automatic"])
seller = c1.selectbox("Seller type", ["Individual", "Dealer", "Trustmark Dealer"])
owner = c2.selectbox("Owner", ["First Owner", "Second Owner", "Third Owner",
                               "Fourth & Above Owner", "Test Drive Car"])

if st.button("Predict price", type="primary"):
    try:
        price = predict_price(f"{brand} {model_name}", year, int(km), fuel, seller, transmission, owner)
        st.success(f"Estimated price: ₹ {price:,.0f}  (≈ {price / 1e5:.2f} lakh)")
    except FileNotFoundError as e:
        st.error(str(e))
