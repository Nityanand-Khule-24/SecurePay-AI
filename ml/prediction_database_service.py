from ml.prediction import predict_fraud
from database.fraud_prediction_service import insert_fraud_prediction


def predict_and_store(transaction_id, transaction_features):

    result = predict_fraud(transaction_features)

    prediction_data = {
        "transaction_id": transaction_id,
        "fraud_probability": result["fraud_probability"],
        "prediction": result["prediction"],
        "risk_level": result["risk_level"],
        "model_version": "RandomForest-v1"
    }

    stored_prediction = insert_fraud_prediction(
        prediction_data
    )

    return {
        "transaction_id": transaction_id,
        "prediction": result["prediction"],
        "fraud_probability": result["fraud_probability"],
        "risk_level": result["risk_level"],
        "database_record": stored_prediction
    }