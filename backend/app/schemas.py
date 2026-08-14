from pydantic import BaseModel


class TransactionRequest(BaseModel):

    transaction_id:int

    type: str
    amount: float

    oldbalanceorg: float
    newbalanceorig: float

    oldbalancedest: float
    newbalancedest: float

    large_transaction: int

    sender_transaction_count: int
    previous_sender_amount: float

    receiver_transaction_count: int
    previous_receiver_amount: float

    previous_receiver_fraud: int
    historical_receiver_fraud_rate: float

    sender_balance_change: float
    receiver_balance_change: float

    balance_ratio: float

    hour: int
    night_transaction: int

    historical_receiver_risk_score: float