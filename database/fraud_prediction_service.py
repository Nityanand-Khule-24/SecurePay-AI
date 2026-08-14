from database.connection import supabase


def insert_fraud_prediction(data):
    """
    Insert ML fraud prediction into Supabase.
    """

    response = (
        supabase
        .table("fraud_predictions")
        .insert(data)
        .execute()
    )

    return response.data


def get_prediction_by_transaction(transaction_id):
    """
    Get fraud prediction for a transaction.
    """

    response = (
        supabase
        .table("fraud_predictions")
        .select("*")
        .eq("transaction_id", transaction_id)
        .execute()
    )

    return response.data


def get_recent_predictions(limit=10):
    """
    Get recent fraud predictions.
    """

    response = (
        supabase
        .table("fraud_predictions")
        .select("*")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data