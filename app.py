#### This is a FastAPI application that provides:
# Training endpoint - Trains a ML model for network security
# Prediction endpoint - Predicts network security threats based on uploaded data
# Web interface - Shows prediction results in a HTML table

import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)
import pymongo
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.pipeline.training_pipeline import TrainingPipeline

# some fastapi libraries 
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request #for files pulling and alll
from uvicorn import run as app_run #to run the app 
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from network_security.utils.main_utils.utils import load_object

from network_security.utils.ML_utils.model.estimator import NetworkModel


client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from network_security.constants import DATA_INGESTION_COLLECTION_NAME
from network_security.constants import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]


#basic set ups for fast api
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates # reposible to pick up the html templates
templates = Jinja2Templates(directory="./templates")

#this is for homepage
@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train") #this one trains the entire training pipeline
async def train_route():
    try:
        train_pipeline=TrainingPipeline() #initiation of training pipeline
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
# A route that predicts 
@app.post("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)): #uploadfile is part of fastapi 
    try:
        df=pd.read_csv(file.file)
        #print(df)
        preprocesor=load_object("final_model/preprocessor.pkl") #pushed pkl file
        final_model=load_object("final_model/model.pkl") #pushed pkl file
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df) # does transformation , then prediction 
        print(y_pred)
        df['predicted_column'] = y_pred #appending in a new column  
        print(df['predicted_column'])
        #df['predicted_column'].replace(-1, 0)
        #return df.to_json()
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        #print(table_html)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
            raise NetworkSecurityException(e,sys)


#the entrypoint     
if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)
