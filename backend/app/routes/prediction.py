from fastapi import APIRouter, HTTPException

from backend.app.schemas import (
    TransactionRequest,
    NewTransactionRequest
)

from backend.app.services.feature_service import (
    build_features
)

from backend.app.services.prediction_service import (
    predict_fraud
)

from backend.app.services.decision_service import make_decision

from database.transaction_service import (
    insert_transaction
)

from backend.app.services.transaction_status_service import (
    update_transaction_status
)

from backend.app.services.alert_service import (
    create_fraud_alert,
    get_all_alerts,
    get_transaction_alerts,
    get_unresolved_alerts,
    resolve_alert
)

from backend.app.services.transaction_history_service import (
    get_recent_transactions,
    get_complete_transaction
)

from backend.app.services.analytics_service import (
    get_analytics_summary
)

from backend.app.services.dashboard_service import (
    get_dashboard_data
)

router = APIRouter(
    prefix="/prediction",
    tags=["Fraud Prediction"]
)


# =========================================================
# 1. EXISTING PREDICTION ENDPOINT
# =========================================================

@router.post("/predict")
def predict(transaction: TransactionRequest):

    try:

        # -------------------------------------------------
        # Convert Pydantic model to dictionary
        # -------------------------------------------------

        transaction_data = transaction.model_dump()

        # -------------------------------------------------
        # Build 19 ML features
        # -------------------------------------------------

        features = build_features(

            transaction_type=transaction_data["type"],

            amount=transaction_data["amount"],

            oldbalanceorg=transaction_data[
                "oldbalanceorg"
            ],

            newbalanceorig=transaction_data[
                "newbalanceorig"
            ],

            oldbalancedest=transaction_data[
                "oldbalancedest"
            ],

            newbalancedest=transaction_data[
                "newbalancedest"
            ],

            sender_id=transaction_data[
                "sender_id"
            ],

            receiver_id=transaction_data[
                "receiver_id"
            ],

            created_at=transaction_data[
                "created_at"
            ]
        )

        # -------------------------------------------------
        # Run ML prediction
        # -------------------------------------------------

        result = predict_fraud(
            features,
            transaction_id=transaction.transaction_id
        )

        # -------------------------------------------------
        # Return prediction
        # -------------------------------------------------

        return {

            "status": "success",

            "transaction_id":
                transaction.transaction_id,

            "prediction":
                result["prediction"],

            "fraud_probability":
                result["fraud_probability"],

            "risk_level":
                result["risk_level"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# 2. NEW TRANSACTION PROCESSING ENDPOINT
# =========================================================

@router.post("/process")
def process_transaction(
    transaction: NewTransactionRequest
):

    try:

        # =============================================
        # 1. Create database transaction record
        # =============================================

        transaction_data = {
            "step": None,

            "transaction_type": transaction.type,

            "amount": transaction.amount,

            "sender_id": transaction.sender_id,

            "receiver_id": transaction.receiver_id,

            "sender_balance_before":
                transaction.oldbalanceorg,

            "sender_balance_after":
                transaction.newbalanceorig,

            "receiver_balance_before":
                transaction.oldbalancedest,

            "receiver_balance_after":
                transaction.newbalancedest,

            # New transaction has no known fraud label yet
            "is_fraud": None,

            "created_at":
                transaction.created_at.isoformat()
        }

        # =============================================
        # 2. Insert transaction
        # =============================================

        inserted_transaction = insert_transaction(
            transaction_data
        )

        if not inserted_transaction:

            raise Exception(
                "Transaction was not inserted into database"
            )

        # =============================================
        # 3. Get generated transaction ID
        # =============================================

        transaction_id = inserted_transaction[0][
            "transaction_id"
        ]

        # =============================================
        # 4. Build 19 ML features
        # =============================================

        features = build_features(

            transaction_type=transaction.type,

            amount=transaction.amount,

            oldbalanceorg=transaction.oldbalanceorg,

            newbalanceorig=transaction.newbalanceorig,

            oldbalancedest=transaction.oldbalancedest,

            newbalancedest=transaction.newbalancedest,

            sender_id=transaction.sender_id,

            receiver_id=transaction.receiver_id,

            created_at=transaction.created_at
        )

        # =============================================
        # 5. Run fraud prediction
        # =============================================

        prediction_result = predict_fraud(
            features,
            transaction_id=transaction_id
        )

        decision_result = make_decision(
            prediction=prediction_result["prediction"],
            fraud_probability=prediction_result["fraud_probability"],
            risk_level=prediction_result["risk_level"]
        )

        # =============================================
        # Create fraud alert
        # =============================================

        alert_result = create_fraud_alert(
            transaction_id=transaction_id,
            decision=decision_result["decision"]
        )
        # =============================================
        # Update transaction status
        # =============================================

        decision = decision_result["decision"]

        if decision == "SAFE":

            transaction_status = "SAFE"

        elif decision == "REVIEW":

            transaction_status = "REVIEW"

        elif decision == "BLOCK":

            transaction_status = "BLOCKED"

        else:

            transaction_status = "PENDING"


        update_transaction_status(
            transaction_id=transaction_id,
            status=transaction_status
        )

        # =============================================
        # 6. Return result
        # =============================================

        return {

            "status": "success",

            "transaction_id":
                transaction_id,

            "prediction":
                prediction_result["prediction"],

            "fraud_probability":
                prediction_result[
                    "fraud_probability"
                ],

            "risk_level":
                prediction_result[
                    "risk_level"
                ],

            "decision":
                decision_result["decision"],

            "action":
                decision_result["action"],

            "alert":
                decision_result["alert"],

            "transaction_status": transaction_status,

            "alert_record": alert_result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =========================================================
# 3. GET RECENT TRANSACTIONS
# =========================================================

@router.get("/transactions")
def get_transactions(limit: int = 20):

    try:

        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=400,
                detail="Limit must be between 1 and 100"
            )

        transactions = get_recent_transactions(
            limit=limit
        )

        return {
            "status": "success",
            "count": len(transactions),
            "transactions": transactions
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# 4. GET COMPLETE TRANSACTION DETAILS
# =========================================================

@router.get("/transactions/{transaction_id}")
def get_transaction_details(
    transaction_id: int
):

    try:

        result = get_complete_transaction(
            transaction_id
        )

        if result is None:

            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )

        return {
            "status": "success",
            **result
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# =========================================================
# 5. ANALYTICS SUMMARY
# =========================================================

@router.get("/analytics/summary")
def analytics_summary():

    try:

        result = get_analytics_summary()

        return {
            "status": "success",
            "analytics": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# =========================================================
# 6. RISK DISTRIBUTION
# =========================================================

@router.get("/analytics/risk-distribution")
def risk_distribution():

    try:

        result = get_analytics_summary()

        return {
            "status": "success",
            "risk_distribution":
                result["risk_distribution"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# =========================================================
# 7. GET ALL FRAUD ALERTS
# =========================================================

@router.get("/alerts")
def get_alerts():

    try:

        alerts = get_all_alerts()

        return {
            "status": "success",
            "count": len(alerts),
            "alerts": alerts
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# =========================================================
# 8. GET UNRESOLVED ALERTS
# =========================================================

@router.get("/alerts/unresolved")
def get_unresolved():

    try:

        alerts = get_unresolved_alerts()

        return {
            "status": "success",
            "count": len(alerts),
            "alerts": alerts
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# =========================================================
# 9. GET TRANSACTION ALERTS
# =========================================================

@router.get("/alerts/{transaction_id}")
def get_alerts_for_transaction(
    transaction_id: int
):

    try:

        alerts = get_transaction_alerts(
            transaction_id
        )

        return {
            "status": "success",
            "transaction_id": transaction_id,
            "count": len(alerts),
            "alerts": alerts
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# =========================================================
# 10. RESOLVE ALERT
# =========================================================

@router.patch("/alerts/{alert_id}/resolve")
def resolve_fraud_alert(
    alert_id: int
):

    try:

        result = resolve_alert(
            alert_id
        )

        if not result:

            raise HTTPException(
                status_code=404,
                detail="Alert not found"
            )

        return {
            "status": "success",
            "message": "Alert resolved successfully",
            "alert": result
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# =========================================================
# 11. DASHBOARD DATA
# =========================================================

@router.get("/dashboard")
def dashboard(
    transaction_limit: int = 10,
    alert_limit: int = 10
):

    try:

        # -------------------------------------------------
        # Validate limits
        # -------------------------------------------------

        if transaction_limit < 1 or transaction_limit > 100:
            raise HTTPException(
                status_code=400,
                detail="transaction_limit must be between 1 and 100"
            )

        if alert_limit < 1 or alert_limit > 100:
            raise HTTPException(
                status_code=400,
                detail="alert_limit must be between 1 and 100"
            )

        # -------------------------------------------------
        # Get dashboard data
        # -------------------------------------------------

        result = get_dashboard_data(
            transaction_limit=transaction_limit,
            alert_limit=alert_limit
        )

        # -------------------------------------------------
        # Return dashboard
        # -------------------------------------------------

        return {
            "status": "success",
            "dashboard": result
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )