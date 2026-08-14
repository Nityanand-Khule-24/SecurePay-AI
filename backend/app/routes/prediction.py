from fastapi import APIRouter, HTTPException

from backend.app.schemas import TransactionRequest
from backend.app.services.prediction_service import predict_fraud

router = APIRouter(
    prefix="/prediction",
    tags=["Fraud Prediction"]
)

@router.post("/predict")
def predict(transaction: TransactionRequest):
    try:
        #convert pydantic model dictionary 
        transaction_date = transaction.model_dump()

        #run ml prediction
        result = predict_fraud(
            transaction_date,
            transaction_id=transaction.transaction_id
         )

        return{
            "status":"success",
            "transaction_id":transaction.transaction_id,
            "prediction":result["prediction"],
            "fraud_probability":result["fraud_probability"],
            "risk_level":result["risk_level"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )