// =========================================================
// SECUREPAY AI API CONFIGURATION
// =========================================================

const API_BASE_URL = "http://127.0.0.1:8000";


// =========================================================
// GENERIC API REQUEST
// =========================================================

async function apiRequest(
    endpoint,
    options = {}
) {

    const url =
        `${API_BASE_URL}${endpoint}`;

    const response =
        await fetch(url, {

            ...options,

            headers: {

                "Content-Type":
                    "application/json",

                ...(options.headers || {})
            }
        });


    if (!response.ok) {

        let errorMessage =
            `API Error: ${response.status}`;

        try {

            const errorData =
                await response.json();

            if (errorData.detail) {

                errorMessage =
                    errorData.detail;
            }

        } catch (error) {

            // Ignore JSON parsing error
        }

        throw new Error(
            errorMessage
        );
    }


    return response.json();
}


// =========================================================
// GET DASHBOARD
// =========================================================

async function getDashboard() {

    return apiRequest(
        "/prediction/dashboard"
    );
}


// =========================================================
// GET ANALYTICS SUMMARY
// =========================================================

async function getAnalyticsSummary() {

    return apiRequest(
        "/prediction/analytics/summary"
    );
}


// =========================================================
// GET RISK DISTRIBUTION
// =========================================================

async function getRiskDistribution() {

    return apiRequest(
        "/prediction/analytics/risk-distribution"
    );
}


// =========================================================
// GET ALERTS
// =========================================================

async function getAlerts() {

    return apiRequest(
        "/prediction/alerts"
    );
}


// =========================================================
// GET UNRESOLVED ALERTS
// =========================================================

async function getUnresolvedAlerts() {

    return apiRequest(
        "/prediction/alerts/unresolved"
    );
}


// =========================================================
// PROCESS TRANSACTION
// =========================================================

async function processTransaction(
    transaction
) {

    return apiRequest(
        "/prediction/process",
        {

            method: "POST",

            body: JSON.stringify(
                transaction
            )
        }
    );
}


// =========================================================
// DASHBOARD LOADER
// =========================================================

async function loadDashboard() {

    try {

        const dashboard =
            await getDashboard();

        console.log(
            "Dashboard:",
            dashboard
        );

    } catch (error) {

        console.error(
            "Dashboard API Error:",
            error
        );
    }
}


// =========================================================
// INITIAL LOAD
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadDashboard();

    }
);