from database.connection import supabase


# =========================================================
# GET RECEIVER HISTORY
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
# CALCULATE RECEIVER RISK
# =========================================================

def calculate_receiver_risk(receiver_id):

    history = get_receiver_history(receiver_id)

    # -----------------------------------------------------
    # No history
    # -----------------------------------------------------

    if not history:

        return {
            "receiver_id": receiver_id,
            "transaction_count": 0,
            "previous_fraud": 0,
            "historical_fraud_rate": 0.0,
            "risk_score": 0.0
        }

    # -----------------------------------------------------
    # Transaction count
    # -----------------------------------------------------

    transaction_count = len(history)

    # -----------------------------------------------------
    # Fraud count
    # -----------------------------------------------------

    previous_fraud = sum(
        int(transaction["is_fraud"])
        for transaction in history
    )

    # -----------------------------------------------------
    # Historical fraud rate
    # -----------------------------------------------------

    historical_fraud_rate = (
        previous_fraud / transaction_count
    )

    # -----------------------------------------------------
    # Risk score
    #
    # Current temporary scoring:
    # fraud rate contributes 60%
    # transaction activity contributes 20%
    # amount activity contributes 20%
    #
    # Dataset-wide normalization will be added after
    # we connect the training statistics.
    # -----------------------------------------------------

    fraud_score = historical_fraud_rate

    transaction_score = 1.0
    amount_score = 1.0

    risk_score = (
        fraud_score * 60
        + transaction_score * 20
        + amount_score * 20
    )

    risk_score = round(risk_score, 2)

    return {
        "receiver_id": receiver_id,
        "transaction_count": transaction_count,
        "previous_fraud": previous_fraud,
        "historical_fraud_rate": historical_fraud_rate,
        "risk_score": risk_score
    }


# =========================================================
# SAVE RECEIVER RISK
# =========================================================

def save_receiver_risk(receiver_risk):

    response = (
        supabase
        .table("receiver_risk")
        .upsert(
            receiver_risk,
            on_conflict="receiver_id"
        )
        .execute()
    )

    return response.data


# =========================================================
# UPDATE RECEIVER RISK
# =========================================================

def update_receiver_risk(receiver_id):

    receiver_risk = calculate_receiver_risk(
        receiver_id
    )

    result = save_receiver_risk(
        receiver_risk
    )

    return result


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    receiver_id = "C_TEST_002"

    print("\n========== RECEIVER RISK ==========\n")

    risk = calculate_receiver_risk(
        receiver_id
    )

    print(risk)

    print("\nSaving receiver risk...\n")

    result = save_receiver_risk(
        risk
    )

    print(result)

    print("\n===================================\n")