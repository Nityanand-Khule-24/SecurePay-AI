from connection import supabase

data = {
    "step":1,
    "transaction_type":"TRANSFER",
    "amount":5000.00,
    "sender_id":"C_TEST_001",
    "receiver_id":"C_TEST_002",
    "sender_balance_before":10000.00,
    "sender_balance_after":5000.00,
    "receiver_balance_before":2000.00,
    "receiver_balance_after":7000.00,
    "is_fraud":0
}

response = supabase.table("transactions").insert(data).execute()

print("transaction inserted successfully")
print(response.data)