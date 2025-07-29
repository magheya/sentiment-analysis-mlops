FROM python:3.11

WORKDIR /frontend

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "front.py", "--server.port=8501", "--server.address=0.0.0.0"]