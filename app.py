import os
import sys
import certifi
import pymongo
import pandas as pd
from dotenv import load_dotenv

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME

from uvicorn import run as app_run

# Load environment variables
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

# Setup MongoDB connection
ca = certifi.where()
client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
db = client[DATA_INGESTION_DATABASE_NAME]
collection = db[DATA_INGESTION_COLLECTION_NAME]

# FastAPI App Setup
app = FastAPI()

# CORS Middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Template Rendering
templates = Jinja2Templates(directory="./templates")

# Root Route - Redirect to Swagger Docs
@app.get("/", tags=['authentication'])
async def index():
    return RedirectResponse(url="/docs")

# Model Training Route
@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful!")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

# Prediction Route (Corrected to `POST` for File Upload)
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        # Load CSV File
        df = pd.read_csv(file.file)
        
        # Load Preprocessor & Model
        preprocessor = load_object("final_models/preprocessor.pkl")
        final_model = load_object("final_models/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        # Make Predictions
        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred
        df.to_csv("prediction_output/output.csv", index=False)

        # Convert DataFrame to HTML Table for Response
        table_html = df.to_html(classes="table table-striped")
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        raise NetworkSecurityException(e, sys)

# Run FastAPI Server
if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)
