import streamlit as st
import requests
import os

API_URL = "https://sentiment-api-n94n.onrender.com/predict"


st.title("Sentiment Analysis")

st.write("Enter a sentence to analyze its sentiment:")

text_input = st.text_area("Input Text", height=150)

if st.button("Analyze Sentiment"):
    if not text_input.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(API_URL, json={"text": text_input})
                if response.status_code == 200:
                    result = response.json()
                    label = result["prediction"]["label"]
                    score = result["prediction"]["score"]
                    st.success(f"Prediction: {label} ({score:.2f})")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Could not connect to API: {e}")
