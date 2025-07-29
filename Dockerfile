# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /sentiment-mlops

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy everything else
COPY . .

# Expose ports
EXPOSE 8000  
EXPOSE 8501

# Start both the FastAPI backend and Streamlit frontend
CMD ["bash", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run front.py --server.port=8501 --server.address=0.0.0.0"]
