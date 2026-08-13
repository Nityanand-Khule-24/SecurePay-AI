from prediction import predict_fraud


# --------------------------------------------------
# Test transaction
# --------------------------------------------------

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


# --------------------------------------------------
# Prediction
# --------------------------------------------------

result = predict_fraud(transaction)


print("\n========== FRAUD PREDICTION ==========")

print(
    "Prediction:",
    result["prediction"]
)

print(
    "Fraud Probability:",
    result["fraud_probability"]
)

print(
    "Risk Level:",
    result["risk_level"]
)