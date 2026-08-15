from datetime import datetime

from database.connection import supabase

from backend.app.services.receiver_service import (
    calculate_receiver_risk
)


# =========================================================
# 1. GET RECEIVER HISTORY
# =========================================================

def get_receiver_history(receiver_id):

    response = (
        supabase
        .table("transactions")
        .select("*")
        .eq("receiver_id", receiver_id)
        .execute()
    )

    return response.data


# =========================================================
# 2. GET SENDER HISTORY
# =========================================================

def get_sender_history(sender_id):

    response = (
        supabase
        .table("transactions")
        .select("*")
        .eq("sender_id", sender_id)
        .execute()
    )

    return response.data


# =========================================================
# 3. GET STORED RECEIVER RISK
# =========================================================

def get_receiver_risk(receiver_id):

    response = (
        supabase
        .table("receiver_risk")
        .select("*")
        .eq("receiver_id", receiver_id)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None


# =========================================================
# 4. CALCULATE HISTORY FEATURES
# =========================================================

def calculate_history_features(
    sender_history,
    receiver_history
):

    # -----------------------------------------------------
    # Sender transaction count
    # -----------------------------------------------------

    sender_transaction_count = len(
        sender_history
    )

    # -----------------------------------------------------
    # Previous sender amount
    # -----------------------------------------------------

    if sender_history:
        previous_sender_amount = float(
            sender_history[-1]["amount"]
        )
    else:
        previous_sender_amount = 0.0

    # -----------------------------------------------------
    # Receiver transaction count
    # -----------------------------------------------------

    receiver_transaction_count = len(
        receiver_history
    )

    # -----------------------------------------------------
    # Previous receiver amount
    # -----------------------------------------------------

    if receiver_history:
        previous_receiver_amount = float(
            receiver_history[-1]["amount"]
        )
    else:
        previous_receiver_amount = 0.0

    # -----------------------------------------------------
    # Previous receiver fraud
    # -----------------------------------------------------

    previous_receiver_fraud = sum(
        int(transaction["is_fraud"])
        for transaction in receiver_history
    )

    # -----------------------------------------------------
    # Historical receiver fraud rate
    # -----------------------------------------------------

    if receiver_transaction_count > 0:

        historical_receiver_fraud_rate = (
            previous_receiver_fraud
            / receiver_transaction_count
        )

    else:

        historical_receiver_fraud_rate = 0.0

    return {
        "sender_transaction_count":
            sender_transaction_count,

        "previous_sender_amount":
            previous_sender_amount,

        "receiver_transaction_count":
            receiver_transaction_count,

        "previous_receiver_amount":
            previous_receiver_amount,

        "previous_receiver_fraud":
            previous_receiver_fraud,

        "historical_receiver_fraud_rate":
            historical_receiver_fraud_rate
    }


# =========================================================
# 5. CALCULATE TRANSACTION FEATURES
# =========================================================

def calculate_transaction_features(
    amount,
    oldbalanceorg,
    newbalanceorig,
    oldbalancedest,
    newbalancedest,
    created_at
):

    # -----------------------------------------------------
    # Large transaction
    # -----------------------------------------------------

    large_transaction = int(
        amount > 100000
    )

    # -----------------------------------------------------
    # Sender balance change
    # -----------------------------------------------------

    sender_balance_change = (
        oldbalanceorg - newbalanceorig
    )

    # -----------------------------------------------------
    # Receiver balance change
    # -----------------------------------------------------

    receiver_balance_change = (
        newbalancedest - oldbalancedest
    )

    # -----------------------------------------------------
    # Balance ratio
    # -----------------------------------------------------

    balance_ratio = (
        amount / (oldbalanceorg + 1)
    )

    # -----------------------------------------------------
    # Transaction hour
    # -----------------------------------------------------

    hour = created_at.hour

    # -----------------------------------------------------
    # Night transaction
    # -----------------------------------------------------

    night_transaction = int(
        0 <= hour <= 5
    )

    return {
        "large_transaction":
            large_transaction,

        "sender_balance_change":
            sender_balance_change,

        "receiver_balance_change":
            receiver_balance_change,

        "balance_ratio":
            balance_ratio,

        "hour":
            hour,

        "night_transaction":
            night_transaction
    }


# =========================================================
# 6. BUILD COMPLETE FEATURES
# =========================================================

def build_features(
    transaction_type,
    amount,
    oldbalanceorg,
    newbalanceorig,
    oldbalancedest,
    newbalancedest,
    sender_id,
    receiver_id,
    created_at
):

    # -----------------------------------------------------
    # Get transaction history
    # -----------------------------------------------------

    sender_history = get_sender_history(
        sender_id
    )

    receiver_history = get_receiver_history(
        receiver_id
    )

    # -----------------------------------------------------
    # Historical features
    # -----------------------------------------------------

    history_features = calculate_history_features(
        sender_history,
        receiver_history
    )

    # -----------------------------------------------------
    # Transaction features
    # -----------------------------------------------------

    transaction_features = (
        calculate_transaction_features(
            amount=amount,
            oldbalanceorg=oldbalanceorg,
            newbalanceorig=newbalanceorig,
            oldbalancedest=oldbalancedest,
            newbalancedest=newbalancedest,
            created_at=created_at
        )
    )

    # -----------------------------------------------------
    # Get receiver risk
    # -----------------------------------------------------

    receiver_risk = get_receiver_risk(
        receiver_id
    )

    # -----------------------------------------------------
    # If receiver risk does not exist,
    # calculate and save it
    # -----------------------------------------------------

    if receiver_risk is None:

        calculate_receiver_risk(
            receiver_id
        )

        receiver_risk = get_receiver_risk(
            receiver_id
        )

    # -----------------------------------------------------
    # Safety fallback
    # -----------------------------------------------------

    if receiver_risk is None:

        historical_receiver_risk_score = 0.0

    else:

        historical_receiver_risk_score = float(
            receiver_risk["risk_score"]
        )

    # -----------------------------------------------------
    # Combine all 19 features
    # -----------------------------------------------------

    features = {

        "type":
            transaction_type,

        "amount":
            amount,

        "oldbalanceorg":
            oldbalanceorg,

        "newbalanceorig":
            newbalanceorig,

        "oldbalancedest":
            oldbalancedest,

        "newbalancedest":
            newbalancedest,

        "large_transaction":
            transaction_features[
                "large_transaction"
            ],

        "sender_transaction_count":
            history_features[
                "sender_transaction_count"
            ],

        "previous_sender_amount":
            history_features[
                "previous_sender_amount"
            ],

        "receiver_transaction_count":
            history_features[
                "receiver_transaction_count"
            ],

        "previous_receiver_amount":
            history_features[
                "previous_receiver_amount"
            ],

        "previous_receiver_fraud":
            history_features[
                "previous_receiver_fraud"
            ],

        "historical_receiver_fraud_rate":
            history_features[
                "historical_receiver_fraud_rate"
            ],

        "sender_balance_change":
            transaction_features[
                "sender_balance_change"
            ],

        "receiver_balance_change":
            transaction_features[
                "receiver_balance_change"
            ],

        "balance_ratio":
            transaction_features[
                "balance_ratio"
            ],

        "hour":
            transaction_features[
                "hour"
            ],

        "night_transaction":
            transaction_features[
                "night_transaction"
            ],

        "historical_receiver_risk_score":
            historical_receiver_risk_score
    }

    return features


# =========================================================
# 7. TEST
# =========================================================

if __name__ == "__main__":

    features = build_features(

        transaction_type="TRANSFER",

        amount=5000.0,

        oldbalanceorg=10000.0,

        newbalanceorig=5000.0,

        oldbalancedest=2000.0,

        newbalancedest=7000.0,

        sender_id="C_TEST_001",

        receiver_id="C_TEST_002",

        created_at=datetime.now()
    )

    print(
        "\n========== COMPLETE FEATURES ==========\n"
    )

    for key, value in features.items():

        print(
            f"{key}: {value}"
        )

    print(
        "\n=======================================\n"
    )

    print(
        f"Total features: {len(features)}"
    )