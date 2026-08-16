from database.connection import supabase


# =========================================================
# GET ALL TRANSACTIONS
# =========================================================

def get_all_transactions():

    response = (
        supabase
        .table("transactions")
        .select("*")
        .execute()
    )

    return response.data


# =========================================================
# GET ALL PREDICTIONS
# =========================================================

def get_all_predictions():

    response = (
        supabase
        .table("fraud_predictions")
        .select("*")
        .execute()
    )

    return response.data


# =========================================================
# GET ALL ALERTS
# =========================================================

def get_all_alerts():

    response = (
        supabase
        .table("fraud_alerts")
        .select("*")
        .execute()
    )

    return response.data


# =========================================================
# ANALYTICS SUMMARY
# =========================================================

def get_analytics_summary():

    transactions = get_all_transactions()

    predictions = get_all_predictions()

    alerts = get_all_alerts()

    # -----------------------------------------------------
    # Transaction counts
    # -----------------------------------------------------

    total_transactions = len(
        transactions
    )

    safe_transactions = sum(
        1
        for transaction in transactions
        if transaction.get("status") == "SAFE"
    )

    review_transactions = sum(
        1
        for transaction in transactions
        if transaction.get("status") == "REVIEW"
    )

    blocked_transactions = sum(
        1
        for transaction in transactions
        if transaction.get("status") == "BLOCKED"
    )

    pending_transactions = sum(
        1
        for transaction in transactions
        if transaction.get("status") == "PENDING"
        or transaction.get("status") is None
    )

    # -----------------------------------------------------
    # Fraud predictions
    # -----------------------------------------------------

    total_predictions = len(
        predictions
    )

    fraud_predictions = sum(
        1
        for prediction in predictions
        if prediction.get("prediction") == 1
    )

    legitimate_predictions = sum(
        1
        for prediction in predictions
        if prediction.get("prediction") == 0
    )

    # -----------------------------------------------------
    # Fraud probability
    # -----------------------------------------------------

    probabilities = [
        float(prediction["fraud_probability"])
        for prediction in predictions
        if prediction.get(
            "fraud_probability"
        ) is not None
    ]

    if probabilities:

        average_fraud_probability = (
            sum(probabilities)
            / len(probabilities)
        )

    else:

        average_fraud_probability = 0.0

    # -----------------------------------------------------
    # Transaction amount
    # -----------------------------------------------------

    amounts = [
        float(transaction["amount"])
        for transaction in transactions
        if transaction.get("amount") is not None
    ]

    total_transaction_amount = (
        sum(amounts)
        if amounts
        else 0.0
    )

    average_transaction_amount = (
        total_transaction_amount
        / len(amounts)
        if amounts
        else 0.0
    )

    # -----------------------------------------------------
    # Risk distribution
    # -----------------------------------------------------

    low_risk = sum(
        1
        for prediction in predictions
        if prediction.get("risk_level") == "LOW"
    )

    medium_risk = sum(
        1
        for prediction in predictions
        if prediction.get("risk_level") == "MEDIUM"
    )

    high_risk = sum(
        1
        for prediction in predictions
        if prediction.get("risk_level") == "HIGH"
    )

    # -----------------------------------------------------
    # Alerts
    # -----------------------------------------------------

    total_alerts = len(
        alerts
    )

    unresolved_alerts = sum(
        1
        for alert in alerts
        if alert.get("is_resolved") is False
    )

    resolved_alerts = sum(
        1
        for alert in alerts
        if alert.get("is_resolved") is True
    )

    # -----------------------------------------------------
    # Return analytics
    # -----------------------------------------------------

    return {

        "transactions": {

            "total":
                total_transactions,

            "safe":
                safe_transactions,

            "review":
                review_transactions,

            "blocked":
                blocked_transactions,

            "pending":
                pending_transactions
        },

        "predictions": {

            "total":
                total_predictions,

            "fraud":
                fraud_predictions,

            "legitimate":
                legitimate_predictions,

            "average_fraud_probability":
                round(
                    average_fraud_probability,
                    4
                )
        },

        "amounts": {

            "total_transaction_amount":
                round(
                    total_transaction_amount,
                    2
                ),

            "average_transaction_amount":
                round(
                    average_transaction_amount,
                    2
                )
        },

        "risk_distribution": {

            "LOW":
                low_risk,

            "MEDIUM":
                medium_risk,

            "HIGH":
                high_risk
        },

        "alerts": {

            "total":
                total_alerts,

            "unresolved":
                unresolved_alerts,

            "resolved":
                resolved_alerts
        }
    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print(
        "\n========== SECUREPAY ANALYTICS ==========\n"
    )

    result = get_analytics_summary()

    print(result)

    print(
        "\n==========================================\n"
    )