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

from database.transaction_service import (
    insert_transaction
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
            "is_fraud": 0,

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
                ]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )