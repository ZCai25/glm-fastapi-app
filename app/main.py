import json
import pickle
from typing import Optional

import os
import sys

import pandas as pd
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

# Get the current script's directory
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Add the project directory to sys.path
project_dir = os.path.abspath(os.path.join(current_script_dir, '../..'))
sys.path.append(project_dir)

# import data preprocessing modules
from app.model.model_utils import transform_and_select_features, selected_features

# Get the current script's directory
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the model file
model_file_path = os.path.join(current_script_dir, 'model', 'model.pkl')

# Load the pre-trained model
with open(model_file_path, 'rb') as file:
    model = pickle.load(file)

# Define FastAPI app
app = FastAPI()

# Defind data classes
class Data(BaseModel):
    x0: Optional[float]
    x1: Optional[float]
    x2: Optional[float]
    x3: Optional[float]
    x4: Optional[float]
    x5: Optional[str]
    x6: Optional[float]
    x7: Optional[float]
    x8: Optional[float]
    x9: Optional[float]
    x10: Optional[float]
    x11: Optional[float]
    x12: Optional[str]
    x13: Optional[float]
    x14: Optional[float]
    x15: Optional[float]
    x16: Optional[float]
    x17: Optional[float]
    x18: Optional[float]
    x19: Optional[float]
    x20: Optional[float]
    x21: Optional[float]
    x22: Optional[float]
    x23: Optional[float]
    x24: Optional[float]
    x25: Optional[float]
    x26: Optional[float]
    x27: Optional[float]
    x28: Optional[float]
    x29: Optional[float]
    x30: Optional[float]
    x31: Optional[str]
    x32: Optional[float]
    x33: Optional[float]
    x34: Optional[float]
    x35: Optional[float]
    x36: Optional[float]
    x37: Optional[float]
    x38: Optional[float]
    x39: Optional[float]
    x40: Optional[float]
    x41: Optional[float]
    x42: Optional[float]
    x43: Optional[float]
    x44: Optional[float]
    x45: Optional[float]
    x46: Optional[float]
    x47: Optional[float]
    x48: Optional[float]
    x49: Optional[float]
    x50: Optional[float]
    x51: Optional[float]
    x52: Optional[float]
    x53: Optional[float]
    x54: Optional[float]
    x55: Optional[float]
    x56: Optional[float]
    x57: Optional[float]
    x58: Optional[float]
    x59: Optional[float]
    x60: Optional[float]
    x61: Optional[float]
    x62: Optional[float]
    x63: Optional[str]
    x64: Optional[float]
    x65: Optional[float]
    x66: Optional[float]
    x67: Optional[float]
    x68: Optional[float]
    x69: Optional[float]
    x70: Optional[float]
    x71: Optional[float]
    x72: Optional[float]
    x73: Optional[float]
    x74: Optional[float]
    x75: Optional[float]
    x76: Optional[float]
    x77: Optional[float]
    x78: Optional[float]
    x79: Optional[float]
    x80: Optional[float]
    x81: Optional[str]
    x82: Optional[str]
    x83: Optional[float]
    x84: Optional[float]
    x85: Optional[float]
    x86: Optional[float]
    x87: Optional[float]
    x88: Optional[float]
    x89: Optional[float]
    x90: Optional[float]
    x91: Optional[float]
    x92: Optional[float]
    x93: Optional[float]
    x94: Optional[float]
    x95: Optional[float]
    x96: Optional[float]
    x97: Optional[float]
    x98: Optional[float]
    x99: Optional[float]


class InputData(BaseModel):
    data: Data


class InputDatas(BaseModel):
    data: list[Data]


# Health check endpoint
@app.get("/")
async def health_check():
    return {"status": "OK", "message": "Health check passed"}

# API endpoint for batch or individual call prediction


@app.post("/predict")
async def predict_batch(data: InputDatas):
    try:
        batch_size = 1000  # Set your desired batch size

        # Process data in batches
        predictions_list = []
        for start in range(0, len(data.data), batch_size):
            end = start + batch_size
            batch_data = data.data[start:end]

            # Convert batch_data to DataFrame
            batch_df = pd.DataFrame(jsonable_encoder(batch_data))

            # Apply data transformation and feature selection
            transformed_data = transform_and_select_features(batch_df)

            # Create a DataFrame with all values set to 0 for selected features
            zero_df = pd.DataFrame(
                0, index=transformed_data.index, columns=list(selected_features))

            # Update the values from the original df for columns that exist in both selected_features and df
            common_features = list(
                set(selected_features).intersection(transformed_data.columns))
            zero_df.update(transformed_data[common_features])

            # Make predictions using the pre-trained model on the zero_df
            threshold = 0.75
            predicted_proba = model.predict(zero_df)
            classified_predictions_list = (
                predicted_proba > threshold).astype(int).tolist()

            # Append predictions to the list
            predictions_list.extend(classified_predictions_list)

        # Define the output format
        output_data = {
            "class_probability": predicted_proba.tolist(),
            "input_variables": selected_features,
            # Example binary classification threshold
            "predicted_class": classified_predictions_list
        }

        print(output_data)

        return output_data

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"prediction error: {str(e)}")


# API endpoint for uploading a JSON file
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        # Parse the content as JSON
        json_content = json.loads(content)
        # # Construct an instance of InputDatas
        input_data = InputDatas(**json_content)
        # Call the batch prediction endpoint with the uploaded data
        result = await predict_batch(input_data)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
