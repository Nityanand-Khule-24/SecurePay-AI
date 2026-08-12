from connection import supabase

def insert_transaction(data):
    """
    insert a transaction into the transaction table 
    """

    response =(
        supabase.table("transactions").insert(data).execute()
    )

    return response.data

def get_transaction(transaction_id):
    """
    get a transaction using its transaction id
    """

    response=(
        supabase.table("transactions").select("*").eq("transaction_id",transaction_id).execute()
    )

    return response.data

def get_recent_transaction(limit=10):
    """
    get the most recent transactions..
    """

    response =(
        supabase.table("transactions").select("*").order("created_at",desc=True).limit(limit).execute()
    )

    return response.data