from database.connection import supabase


# =========================================================
# GET RECENT TRANSACTIONS
# =========================================================

def get_recent_transactions(limit=20):
    """
    Get the most recent transactions.
    """

    response = (
        supabase
        .table("transactions")
        .select("*")
        .order(
            "created_at",
            desc=True
        )
        .limit(limit)
        .execute()
    )

    return response.data


# =========================================================
# GET TRANSACTION BY ID
# =========================================================

def get_transaction_by_id(
    transaction_id
):
    """
    Get a single transaction by transaction ID.
    """

    response = (
        supabase
        .table("transactions")
        .select("*")
        .eq(
            "transaction_id",
            transaction_id
        )
        .execute()
    )

    return response.data


# =========================================================
# GET TRANSACTION PREDICTION
# =========================================================

def get_transaction_prediction(
    transaction_id
):
    """
    Get fraud prediction for a transaction.
    """

    response = (
        supabase
        .table("fraud_predictions")
        .select("*")
        .eq(
            "transaction_id",
            transaction_id
        )
        .order(
            "created_at",
            desc=True
        )
        .limit(1)
        .execute()
    )

    return response.data


# =========================================================
# GET TRANSACTION ALERTS
# =========================================================

def get_transaction_alerts(
    transaction_id
):
    """
    Get alerts associated with a transaction.
    """

    response = (
        supabase
        .table("fraud_alerts")
        .select("*")
        .eq(
            "transaction_id",
            transaction_id
        )
        .order(
            "created_at",
            desc=True
        )
        .execute()
    )

    return response.data


# =========================================================
# GET COMPLETE TRANSACTION DETAILS
# =========================================================

def get_complete_transaction(
    transaction_id
):
    """
    Combine transaction, prediction,
    and alert information.
    """

    transaction = get_transaction_by_id(
        transaction_id
    )

    if not transaction:
        return None

    prediction = get_transaction_prediction(
        transaction_id
    )

    alerts = get_transaction_alerts(
        transaction_id
    )

    return {
        "transaction": transaction[0],
        "prediction": (
            prediction[0]
            if prediction
            else None
        ),
        "alerts": alerts
    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print(
        "\n========== TRANSACTION HISTORY ==========\n"
    )

    transactions = get_recent_transactions(
        limit=10
    )

    print("Recent transactions:")

    for transaction in transactions:
        print(transaction)

    print(
        "\n==========================================\n"
    )