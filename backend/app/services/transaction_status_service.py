from database.connection import supabase


# =========================================================
# UPDATE TRANSACTION STATUS
# =========================================================

def update_transaction_status(
    transaction_id,
    status
):
    """
    Update the business status of a transaction.
    """

    response = (
        supabase
        .table("transactions")
        .update({
            "status": status
        })
        .eq(
            "transaction_id",
            transaction_id
        )
        .execute()
    )

    return response.data


# =========================================================
# GET TRANSACTION STATUS
# =========================================================

def get_transaction_status(
    transaction_id
):
    """
    Get the current status of a transaction.
    """

    response = (
        supabase
        .table("transactions")
        .select(
            "transaction_id,status"
        )
        .eq(
            "transaction_id",
            transaction_id
        )
        .execute()
    )

    return response.data


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    transaction_id = 8

    print(
        "\n========== TRANSACTION STATUS ==========\n"
    )

    result = update_transaction_status(
        transaction_id,
        "PENDING"
    )

    print("Updated:")
    print(result)

    print("\nCurrent status:")

    status = get_transaction_status(
        transaction_id
    )

    print(status)

    print(
        "\n=========================================\n"
    )