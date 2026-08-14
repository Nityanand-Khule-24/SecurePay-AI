from fastapi import FastAPI
from backend.app.routes.prediction import router as prediction_router

app=FastAPI(
    title="SecurePay AI",
    description="UPI Fraud Detection API",
    version="1.0.0"
)

app.include_router(prediction_router)

@app.get("/")
def home():
    return{
        "message":"SecurPay AI API is running",
        "status":"success"
    }