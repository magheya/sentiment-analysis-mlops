import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Sentiment Analysis API is running"}

def test_predict_valid_input(monkeypatch):
    # Mocking the MLflow model's output to avoid actual loading during test
    def mock_pipeline(text):
        return [{"label": "LABEL_1", "score": 0.9876}]

    # Patch the mlflow.transformers.load_model call
    from app import mlflow
    monkeypatch.setattr(mlflow.transformers, "load_model", lambda _: mock_pipeline)

    response = client.post("/predict", json={"text": "This is awesome!"})
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["prediction"]["label"] == "Positive"
    assert isinstance(json_data["prediction"]["score"], float)

def test_predict_exception(monkeypatch):
    def mock_load_model_fail(uri):
        raise RuntimeError("Mocked model loading error")
    
    # Patch the load_model function to raise an error
    monkeypatch.setattr("mlflow.transformers.load_model", mock_load_model_fail)
    
    response = client.post("/predict", json={"text": "Trigger failure"})
    assert response.status_code == 500
    assert response.json()["detail"] == "Mocked model loading error"

def test_predict_long_input(monkeypatch):
    def mock_pipeline(text):
        return [{"label": "LABEL_2", "score": 0.9}]
    
    monkeypatch.setattr("mlflow.transformers.load_model", lambda _: mock_pipeline)

    long_text = "This is great. " * 1000  # very long text input
    response = client.post("/predict", json={"text": long_text})
    assert response.status_code == 200
    assert "prediction" in response.json()

def test_predict_unknown_label(monkeypatch):
    def mock_pipeline(text):
        return [{"label": "LABEL_99", "score": 0.95}]  # Not in label_map.
    
    monkeypatch.setattr("mlflow.transformers.load_model", lambda _: mock_pipeline)

    response = client.post("/predict", json={"text": "Strange output"})
    assert response.status_code == 200
    assert response.json()["prediction"]["label"] == "LABEL_99"

