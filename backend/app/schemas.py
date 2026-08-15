from datetime import datetime

from pydantic import BaseModel


class TransactionRequest(BaseModel):

    transaction_id: int

    type: str
    amount: float

    sender_id: str
    receiver_id: str

    oldbalanceorg: float
    newbalanceorig: float

    oldbalancedest: float
    newbalancedest: float

    created_at: datetime

class NewTransactionRequest(BaseModel):

    type:str
    amount:float

    sender_id:str
    receiver_id:str

    oldbalanceorg:float
    newbalanceorig:float

    oldbalancedest:float
    newbalancedest:float

    created_at:datetime

class BasicTransactionRequest(BaseModel):

    transaction_id: int

    type: str
    amount: float

    sender_id: str
    receiver_id: str