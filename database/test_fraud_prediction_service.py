from fraud_prediction_service import (
    insert_fraud_prediction,
    get_prediction_by_transaction,
    get_recent_predictions
)

prediction = {
    "transaction_id": 5,
    "fraud_probability": 0.02,
    "prediction": 0,
    "risk_level": "LOW",
    "model_version": "RandomForest-v1"
}


#insert prediction 

result = insert_fraud_prediction(prediction)

print("\nfraud prediction inserted:")
print(result)

#retrive prediction
result = get_prediction_by_transaction(5)

print("\nprediction for transaction 5:")
print(result)

#recent predictions
result = get_recent_predictions(5)
print("\nrecent prediction:")
for row in result:
    print(row)