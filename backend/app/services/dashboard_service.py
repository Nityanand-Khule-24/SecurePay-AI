from backend.app.services.analytics_service import (
    get_analytics_summary
)

from backend.app.services.transaction_history_service import (
    get_recent_transactions
)

from backend.app.services.alert_service import (
    get_all_alerts,
    get_unresolved_alerts
)


# =========================================================
# DASHBOARD DATA
# =========================================================

def get_dashboard_data(
    transaction_limit=10,
    alert_limit=10
):
    """
    Collect all important information required
    by the SecurePay AI dashboard.
    """

    # -----------------------------------------------------
    # Analytics
    # -----------------------------------------------------

    analytics = get_analytics_summary()

    # -----------------------------------------------------
    # Recent transactions
    # -----------------------------------------------------

    transactions = get_recent_transactions(
        limit=transaction_limit
    )

    # -----------------------------------------------------
    # All alerts
    # -----------------------------------------------------

    alerts = get_all_alerts()

    # -----------------------------------------------------
    # Unresolved alerts
    # -----------------------------------------------------

    unresolved_alerts = get_unresolved_alerts()

    # -----------------------------------------------------
    # Limit alerts for dashboard
    # -----------------------------------------------------

    recent_alerts = alerts[
        :alert_limit
    ]

    # -----------------------------------------------------
    # Dashboard response
    # -----------------------------------------------------

    return {

        "summary": analytics,

        "recent_transactions":
            transactions,

        "recent_alerts":
            recent_alerts,

        "unresolved_alerts":
            unresolved_alerts
    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print(
        "\n========== SECUREPAY DASHBOARD ==========\n"
    )

    dashboard = get_dashboard_data(
        transaction_limit=10,
        alert_limit=10
    )

    print(dashboard)

    print(
        "\n=========================================\n"
    )