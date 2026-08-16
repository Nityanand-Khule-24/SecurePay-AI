from database.connection import supabase


# =========================================================
# CREATE FRAUD ALERT
# =========================================================

def create_fraud_alert(
    transaction_id,
    decision
):
    """
    Create a fraud alert based on the
    Decision Engine result.

    SAFE   -> No alert
    REVIEW -> MEDIUM alert
    BLOCK  -> HIGH alert
    """

    # -----------------------------------------------------
    # SAFE TRANSACTION
    # -----------------------------------------------------

    if decision == "SAFE":

        return None

    # -----------------------------------------------------
    # REVIEW TRANSACTION
    # -----------------------------------------------------

    elif decision == "REVIEW":

        alert_type = "FRAUD_REVIEW"

        severity = "MEDIUM"

        message = (
            "Transaction requires fraud review"
        )

    # -----------------------------------------------------
    # BLOCKED TRANSACTION
    # -----------------------------------------------------

    elif decision == "BLOCK":

        alert_type = "FRAUD_BLOCKED"

        severity = "HIGH"

        message = (
            "Suspicious transaction blocked "
            "by SecurePay AI"
        )

    # -----------------------------------------------------
    # UNKNOWN DECISION
    # -----------------------------------------------------

    else:

        raise ValueError(
            f"Unknown decision: {decision}"
        )

    # -----------------------------------------------------
    # Alert record
    # -----------------------------------------------------

    alert_data = {

        "transaction_id":
            transaction_id,

        "alert_type":
            alert_type,

        "severity":
            severity,

        "message":
            message,

        "is_resolved":
            False
    }

    # -----------------------------------------------------
    # Save alert
    # -----------------------------------------------------

    response = (
        supabase
        .table("fraud_alerts")
        .insert(alert_data)
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
    Get all alerts associated with
    a specific transaction.
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
# GET ALL ALERTS
# =========================================================

def get_all_alerts():
    """
    Get all fraud alerts.

    Latest alerts are returned first.
    """

    response = (
        supabase
        .table("fraud_alerts")
        .select("*")
        .order(
            "created_at",
            desc=True
        )
        .execute()
    )

    return response.data


# =========================================================
# GET UNRESOLVED ALERTS
# =========================================================

def get_unresolved_alerts():
    """
    Get only unresolved fraud alerts.
    """

    response = (
        supabase
        .table("fraud_alerts")
        .select("*")
        .eq(
            "is_resolved",
            False
        )
        .order(
            "created_at",
            desc=True
        )
        .execute()
    )

    return response.data


# =========================================================
# RESOLVE ALERT
# =========================================================

def resolve_alert(
    alert_id
):
    """
    Mark a fraud alert as resolved.
    """

    response = (
        supabase
        .table("fraud_alerts")
        .update({
            "is_resolved": True
        })
        .eq(
            "alert_id",
            alert_id
        )
        .execute()
    )

    return response.data


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print(
        "\n========== FRAUD ALERT SERVICE TEST ==========\n"
    )

    # -----------------------------------------------------
    # TEST 1: GET ALL ALERTS
    # -----------------------------------------------------

    print("ALL ALERTS:")

    all_alerts = get_all_alerts()

    print(all_alerts)

    # -----------------------------------------------------
    # TEST 2: GET UNRESOLVED ALERTS
    # -----------------------------------------------------

    print("\nUNRESOLVED ALERTS:")

    unresolved_alerts = get_unresolved_alerts()

    print(unresolved_alerts)

    # -----------------------------------------------------
    # TEST 3: SAFE
    # -----------------------------------------------------

    print("\nSAFE TEST:")

    safe_result = create_fraud_alert(
        transaction_id=8,
        decision="SAFE"
    )

    print(safe_result)

    # -----------------------------------------------------
    # TEST 4: REVIEW
    # -----------------------------------------------------

    print("\nREVIEW TEST:")

    review_result = create_fraud_alert(
        transaction_id=8,
        decision="REVIEW"
    )

    print(review_result)

    # -----------------------------------------------------
    # TEST 5: BLOCK
    # -----------------------------------------------------

    print("\nBLOCK TEST:")

    block_result = create_fraud_alert(
        transaction_id=8,
        decision="BLOCK"
    )

    print(block_result)

    print(
        "\n===============================================\n"
    )