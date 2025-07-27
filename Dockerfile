# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /sentiment-mlops

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy everything else
COPY . .

# Expose the port your app runs on
EXPOSE 8080

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
