from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import mlflow
import mlflow.transformers
import os
import logging

class InputText(BaseModel):
    text: str

app = FastAPI()

# Load the model

model_path = os.path.join(os.path.dirname(__file__), '..', 'mlflow_model')
model = mlflow.pyfunc.load_model(model_path)

# Request schema
class TextInput(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "Sentiment Analysis API is running"}

label_map = {"LABEL_0": "Negative", "LABEL_1": "Positive"}

@app.post("/predict")
def predict(input: InputText):
    try:
        # Load model
        model_uri = "mlflow_model"  # or the absolute path if needed
        pipeline = mlflow.transformers.load_model(model_uri)

        # Predict
        result = pipeline(input.text)[0]
        return {
            "input": input.text,
            "prediction": {
                "label": label_map.get(result["label"], result["label"]),
                "score": round(result["score"], 4)
            }
        }

    except Exception as e:
        logging.exception("Prediction error")
        raise HTTPException(status_code=500, detail=str(e))
