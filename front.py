import streamlit as st
import requests

API_URL = "https://sentiment-analysis-mlops-oqe4.onrender.com/predict"  # Update this if your FastAPI backend is hosted elsewhere

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
                result = response.json()

                if response.status_code == 200:
                    result = response.json()
                    prediction = result["prediction"]
                    label = prediction["label"]
                    score = prediction["score"]
                    
                    st.success(f"Prediction: {label} ({score:.2f})")
                else:
                    st.error(f"Error: {result.get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Could not connect to API: {e}")
