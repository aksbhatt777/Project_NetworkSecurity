import sys
import os
import logging
import pandas as pd
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import uvicorn
import certifi
import pymongo

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from network_security.exception.exception import NetworkSecurityException
from network_security.utils.main_utils.utils import load_object
from network_security.utils.ML_utils.model.estimator import NetworkModel

# Initialize FastAPI app
app = FastAPI(
    title="Network Security Prediction API",
    description="ML-based Network Security Threat Detection System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates
templates = Jinja2Templates(directory="./templates")

# Global variables
network_model = None
model_loaded = False

# Model loading on startup
@app.on_event("startup")
async def load_model():
    global network_model, model_loaded
    try:
        logger.info("Loading model...")
        preprocessor = load_object("final_model/preprocessor.pkl")
        model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=model)
        model_loaded = True
        logger.info("Model loaded successfully!")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        model_loaded = False

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model_loaded,
        "service": "Network Security API"
    }

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "model_loaded": model_loaded}
    )

# Prediction endpoint
@app.post("/predict")
async def predict(request: Request, file: UploadFile = File(...)):
    try:
        # Validate file
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are accepted")
        
        # Read CSV
        df = pd.read_csv(file.file)
        logger.info(f"Received file: {file.filename} with {len(df)} rows")
        
        # Check if model is loaded
        if not model_loaded:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Make predictions
        predictions = network_model.predict(df)
        df['predicted_column'] = predictions
        
        # Save output
        os.makedirs('prediction_output', exist_ok=True)
        output_path = f'prediction_output/output_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.csv'
        df.to_csv(output_path, index=False)
        
        # Return HTML table
        table_html = df.to_html(classes='table table-striped', index=False)
        return templates.TemplateResponse(
            "table.html", 
            {"request": request, "table": table_html, "rows": len(df)}
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        workers=int(os.getenv("WORKERS", 1)), # Changed from 4 to 1 for render
        log_level=os.getenv("LOG_LEVEL", "info")
    )