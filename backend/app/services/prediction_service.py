import os
import joblib
import pandas as pd
from database.fraud_prediction_service import insert_fraud_prediction

#project root 
BASE_DIR=os.path.abspath(
    os.path.join(os.path.dirname(__file__),"../../../")
)

#model paths
MODEL_PATH=os.path.join(
    BASE_DIR,
    "ml",
    "models",
    "fraud_model.pkl"
)

ENCODER_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "models",
    "label_encoder.pkl"
)

FEATURE_COLUMNS_PATH= os.path.join(
    BASE_DIR,
    "ml",
    "models",
    "feature_columns.pkl"
)

#load ml components
model=joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)
feature_columns = joblib.load(FEATURE_COLUMNS_PATH)

def predict_fraud(transaction_data, transaction_id=None):
    #convert request data to dataframe 
    df=pd.DataFrame([transaction_data])

    #encode transaction type 
    df["type"]=encoder.transform(df["type"])

    #ensure exact feature order
    df = df[feature_columns]

    #prediction 
    prediction = int(model.predict(df)[0])

    #fraud probability
    probability = float(
        model.predict_proba(df)[0][1]
    )

    #risk level 
    if probability >= 0.70:
        risk_level = "HIGH"

    elif probability >= 0.30:
        risk_level="MEDIUM"

    else:
        risk_level="LOW"

    #store prediction in supabase 
    database_record = None

    if transaction_id is not None:
        prediction_data ={
            "transaction_id":transaction_id,
            "fraud_probability":probability,
            "prediction":prediction,
            "risk_level":risk_level,
            "model_version":"RandomForest-v1"
        }

        database_record=insert_fraud_prediction(
            prediction_data
        )

    return{
        "prediction":prediction,
        "fraud_probability":probability,
        "risk_level":risk_level,
        "database_record":database_record
    }

