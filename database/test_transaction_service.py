from transaction_service import (
    insert_transaction,
    get_transaction,
    get_recent_transaction
)

# testin transactions 
transaction = {
    "step":3,
    "transaction_type":"PAYMENT",
    "amount":1500.00,
    "sender_id":"C_TEST_003",
    "receiver_id":"C_TEST_001",
    "sender_balance_before":5000.00,
    "sender_balance_after":3500.00,
    "receiver_balance_before":1000.00,
    "receiver_balance_after":2500.00,
    "is_fraud":0
}

#insert

result = insert_transaction(transaction)
print("\ntransaction inserted:")
print(result)

#get transaction 
if result:
    transaction_id = result[0]["transaction_id"]
    result=get_transaction(transaction_id)
    print("\ntransaction retrived:")
    print(result)

#get recent transactions
result = get_recent_transaction(5)
print("\nrecent transactions:")
for row in result:
    print(row)