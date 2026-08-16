def make_decision(
    prediction,
    fraud_probability,
    risk_level
):
    """
    Convert ML prediction and risk level
    into a business decision.
    """

    # =========================================
    # HIGH RISK
    # =========================================

    if risk_level == "HIGH":

        return {
            "decision": "BLOCK",
            "action": "Transaction blocked",
            "alert": True
        }

    # =========================================
    # MEDIUM RISK
    # =========================================

    elif risk_level == "MEDIUM":

        return {
            "decision": "REVIEW",
            "action": "Transaction requires review",
            "alert": True
        }

    # =========================================
    # LOW RISK
    # =========================================

    else:

        return {
            "decision": "SAFE",
            "action": "Transaction allowed",
            "alert": False
        }


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    print("\n========== DECISION ENGINE TEST ==========\n")

    low_result = make_decision(
        prediction=0,
        fraud_probability=0.05,
        risk_level="LOW"
    )

    print("LOW:")
    print(low_result)

    medium_result = make_decision(
        prediction=0,
        fraud_probability=0.45,
        risk_level="MEDIUM"
    )

    print("\nMEDIUM:")
    print(medium_result)

    high_result = make_decision(
        prediction=1,
        fraud_probability=0.92,
        risk_level="HIGH"
    )

    print("\nHIGH:")
    print(high_result)

    print("\n==========================================")