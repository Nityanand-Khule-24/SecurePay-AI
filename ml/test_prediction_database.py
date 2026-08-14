from ml.prediction_database_service import predict_and_store

transaction = {
    "type": "TRANSFER",

    "amount": 5000.0,

    "oldbalanceorg": 10000.0,

    "newbalanceorig": 5000.0,

    "oldbalancedest": 2000.0,

    "newbalancedest": 7000.0,

    "large_transaction": 0,

    "sender_transaction_count": 1,

    "previous_sender_amount": 0.0,

    "receiver_transaction_count": 1,

    "previous_receiver_amount": 0.0,

    "previous_receiver_fraud": 0,

    "historical_receiver_fraud_rate": 0.0,

    "sender_balance_change": 5000.0,

    "receiver_balance_change": 5000.0,

    "balance_ratio": 0.5,

    "hour": 18,

    "night_transaction": 0,

    "historical_receiver_risk_score": 0.0
}

result = predict_and_store(
    transaction_id=5,
    transaction_features=transaction
)

print("\n---final result---")
print("Transaction ID:", result["transaction_id"])
print("Prediction:", result["prediction"])
print("Fraud Probability:", result["fraud_probability"])
print("Risk Level:", result["risk_level"])

print("\nDatabase Record:")
print(result["database_record"])