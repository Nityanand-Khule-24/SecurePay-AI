import os
import joblib
import pandas as pd


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "ml",
    "models"
)


# --------------------------------------------------
# Load ML artifacts
# --------------------------------------------------

model = joblib.load(
    os.path.join(
        MODEL_DIR,
        "fraud_model.pkl"
    )
)

encoder = joblib.load(
    os.path.join(
        MODEL_DIR,
        "label_encoder.pkl"
    )
)

feature_columns = joblib.load(
    os.path.join(
        MODEL_DIR,
        "feature_columns.pkl"
    )
)


# --------------------------------------------------
# Verify model
# --------------------------------------------------

if model.n_features_in_ != len(feature_columns):
    raise ValueError(
        f"Model expects {model.n_features_in_} features, "
        f"but feature_columns contains {len(feature_columns)}."
    )


# --------------------------------------------------
# Risk Level
# --------------------------------------------------

def get_risk_level(fraud_probability):

    if fraud_probability >= 0.80:
        return "HIGH"

    elif fraud_probability >= 0.50:
        return "MEDIUM"

    else:
        return "LOW"


# --------------------------------------------------
# Fraud Prediction
# --------------------------------------------------

def predict_fraud(transaction_features):

    df = pd.DataFrame([transaction_features])

    # Check missing features
    missing_features = [
        feature
        for feature in feature_columns
        if feature not in df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Missing features: {missing_features}"
        )

    # Exact feature order used during training
    df = df[feature_columns].copy()

    # Encode transaction type
    df["type"] = encoder.transform(
        df["type"]
    )

    # Prediction
    prediction = int(
        model.predict(df)[0]
    )

    # Probability
    probability = float(
        model.predict_proba(df)[0][1]
    )

    # Risk level
    risk_level = get_risk_level(
        probability
    )

    return {
        "prediction": prediction,
        "fraud_probability": probability,
        "risk_level": risk_level
    }