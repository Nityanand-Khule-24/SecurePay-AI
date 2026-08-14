# SecurePay AI — FastAPI + ML + Supabase Integration

## Step 16 — API → ML → Supabase

### Date
14 August 2026

---

## 1. Objective

The goal of this step was to connect the trained fraud detection model with the FastAPI backend and store the prediction results in Supabase.

The completed flow is:

UPI Transaction
        ↓
FastAPI
        ↓
Pydantic Validation
        ↓
Random Forest Model
        ↓
Fraud Prediction
        ↓
Fraud Probability
        ↓
Risk Level
        ↓
Supabase
        ↓
fraud_predictions

---

# 2. Backend Structure

The existing backend structure was used instead of creating a new API folder.

```text
backend/
└── app/
    ├── routes/
    │   └── prediction.py
    │
    ├── services/
    │   └── prediction_service.py
    │
    ├── utils/
    │
    ├── main.py
    ├── models.py
    ├── schemas.py
    └── crud.py
````

---

# 3. ML Model Used

The trained model created in the previous step was reused.

```text
ml/models/
├── fraud_model.pkl
├── label_encoder.pkl
└── feature_columns.pkl
```

### Model

```text
RandomForestClassifier
```

### Transaction Type Encoder

```text
LabelEncoder
```

Classes:

```text
CASH_IN
CASH_OUT
DEBIT
PAYMENT
TRANSFER
```

### Number of Features

```text
19
```

The model expects these exact features:

```text
1. type
2. amount
3. oldbalanceorg
4. newbalanceorig
5. oldbalancedest
6. newbalancedest
7. large_transaction
8. sender_transaction_count
9. previous_sender_amount
10. receiver_transaction_count
11. previous_receiver_amount
12. previous_receiver_fraud
13. historical_receiver_fraud_rate
14. sender_balance_change
15. receiver_balance_change
16. balance_ratio
17. hour
18. night_transaction
19. historical_receiver_risk_score
```

---

# 4. Pydantic Transaction Schema

A `TransactionRequest` schema was created to validate the API request.

The schema contains the 19 ML features.

A `transaction_id` was also added because the prediction needs to be associated with the original transaction in Supabase.

Example:

```json
{
    "transaction_id": 5,
    "type": "TRANSFER",
    "amount": 5000.0,
    "oldbalanceorg": 10000.0,
    "newbalanceorig": 5000.0,
    "oldbalancedest": 2000.0,
    "newbalancedest": 7000.0,
    "large_transaction": 0,
    "sender_transaction_count": 1,
    "previous_sender_amount": 0.0,
    "receiver_transaction_count": 1,
    "previous_receiver_amount": 0.0,
    "previous_receiver_fraud": 0,
    "historical_receiver_fraud_rate": 0.0,
    "sender_balance_change": 5000.0,
    "receiver_balance_change": 5000.0,
    "balance_ratio": 0.5,
    "hour": 18,
    "night_transaction": 0,
    "historical_receiver_risk_score": 0.0
}
```

---

# 5. ML Prediction Service

The FastAPI backend loads:

```text
fraud_model.pkl
label_encoder.pkl
feature_columns.pkl
```

The prediction service performs the following operations:

```text
Request Data
    ↓
Pandas DataFrame
    ↓
Encode transaction type
    ↓
Arrange exact feature order
    ↓
Random Forest prediction
    ↓
Fraud probability
    ↓
Risk level
```

---

# 6. Risk Level Logic

The fraud probability is converted into a risk level.

```text
Probability >= 0.70
        ↓
HIGH
```

```text
Probability >= 0.30
        ↓
MEDIUM
```

```text
Probability < 0.30
        ↓
LOW
```

The API returns:

```json
{
    "status": "success",
    "transaction_id": 5,
    "prediction": 0,
    "fraud_probability": 0.02,
    "risk_level": "LOW"
}
```

The exact probability depends on the trained Random Forest model.

---

# 7. Supabase Integration

The existing Supabase database service was reused.

Existing service:

```text
database/fraud_prediction_service.py
```

Existing function:

```text
insert_fraud_prediction()
```

The prediction service sends:

```text
transaction_id
fraud_probability
prediction
risk_level
model_version
```

to the Supabase table:

```text
fraud_predictions
```

Example stored record:

```text
transaction_id     → 5
fraud_probability  → model result
prediction         → 0
risk_level         → LOW
model_version      → RandomForest-v1
```

---

# 8. FastAPI Prediction Endpoint

Endpoint created:

```text
POST /prediction/predict
```

Swagger documentation is available through:

```text
http://127.0.0.1:8000/docs
```

The endpoint was successfully tested through Swagger UI.

---

# 9. Important Errors Faced and Solutions

Only meaningful project/integration errors are documented below.

---

## Error 1 — FastAPI Import Error

### Error

```text
ModuleNotFoundError: No module named 'app'
```

### Cause

The FastAPI application was started from the project root using:

```text
uvicorn backend.app.main:app --reload
```

but the internal imports were written as:

```python
from app.routes.prediction import router
```

Python could not find `app` as a top-level package.

### Solution

Changed imports to use the complete package path:

```python
from backend.app.routes.prediction import router
```

Similarly:

```python
from backend.app.schemas import TransactionRequest
from backend.app.services.prediction_service import predict_fraud
```

Also ensured the required `__init__.py` files existed.

### Result

FastAPI started successfully.

---

# 10. Error 2 — Fraud Probability Key Mismatch

### Error

```text
{
    "detail": "'fraud_prabability'"
}
```

### Cause

The API route was trying to access:

```python
result["fraud_prabability"]
```

but the prediction service returned:

```python
result["fraud_probability"]
```

The key names did not match.

### Solution

Changed:

```python
"fraud_prabability"
```

to:

```python
"fraud_probability"
```

### Result

The prediction API returned the correct response.

---

# 11. Previous Supabase Integration Issues

During the earlier Supabase setup, Row Level Security initially blocked inserts.

### Error

```text
new row violates row-level security policy
for table "transactions"
```

### Cause

RLS was enabled but the appropriate insert policy was not yet configured for the API access role.

### Solution

Configured insert policies for the required access roles.

Verified policies:

```text
Allow backend insert transactions
Allow anon insert transactions
```

After the policy configuration, transaction insertion worked successfully.

---

# 12. Supabase Table Name Issue

During fraud prediction service testing, the following error occurred:

```text
Could not find the table 'public.fraud_prediction'
```

Supabase suggested:

```text
public.fraud_predictions
```

### Cause

The Python service used the singular table name:

```text
fraud_prediction
```

while the actual Supabase table was:

```text
fraud_predictions
```

### Solution

Changed the service to use:

```python
supabase.table("fraud_predictions")
```

### Result

Fraud prediction insertion worked successfully.

---

# 13. Supabase Response Access Issue

Another integration issue occurred while retrieving a prediction.

### Error

```text
AttributeError:
'function' object has no attribute 'data'
```

### Cause

The response object was being accessed incorrectly.

The code attempted to access `.data` on a callable/function instead of the executed response.

### Solution

Corrected the Supabase response handling so that `.data` is accessed on the actual executed response.

### Result

Prediction retrieval worked correctly.

---

# 14. Important ML Model Observation

The model directory contained a scaler file, but it was empty.

The model was verified using:

```text
ml/check_model.py
```

The verification showed:

```text
Model:
<class 'sklearn.ensemble._forest.RandomForestClassifier'>

Encoder:
<class 'sklearn.preprocessing._label.LabelEncoder'>

Number of features:
19
```

Because the trained Random Forest pipeline did not use a scaler, the empty scaler file was removed.

The final prediction pipeline uses:

```text
Random Forest
+
Label Encoder
+
Feature Columns
```

No scaler is required.

---

# 15. Final API Architecture

The completed architecture for today's work is:

```text
                UPI Transaction
                       │
                       ▼
                FastAPI Backend
                       │
                       ▼
              Transaction Schema
                       │
                       ▼
             Prediction Service
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
       Label Encoder        Feature Columns
             │                   │
             └─────────┬─────────┘
                       ▼
               Random Forest
                       │
              ┌────────┴────────┐
              ▼                 ▼
        Prediction       Fraud Probability
              │                 │
              └────────┬────────┘
                       ▼
                  Risk Level
                       │
                       ▼
                   Supabase
                       │
                       ▼
             fraud_predictions
```

---

# 16. Technologies Used

```text
Python
FastAPI
Pydantic
Pandas
Scikit-learn
Random Forest
Joblib
Supabase
PostgREST
Uvicorn
Swagger / OpenAPI
```

---

# 17. Current Status

```text
ML Model                         ✅
Model Loading                    ✅
Label Encoding                   ✅
19 Feature Pipeline              ✅
FastAPI Backend                  ✅
Pydantic Validation              ✅
Prediction Endpoint              ✅
Swagger Testing                  ✅
ML Prediction                    ✅
Fraud Probability                ✅
Risk Classification              ✅
Supabase Connection              ✅
Prediction Storage               ✅
API → ML → Supabase              ✅
```

---

# 18. Next Step

The current API requires all 19 engineered ML features from the client.

This is not ideal for a real-world UPI application.

The next step is to create a simpler transaction API where the client sends basic transaction information such as:

```json
{
    "transaction_id": 6,
    "type": "TRANSFER",
    "amount": 5000.0,
    "sender_id": "C123456",
    "receiver_id": "C987654"
}
```

The backend will then generate the required features.

Target architecture:

```text
Basic UPI Transaction
        ↓
Feature Engineering
        ↓
19 ML Features
        ↓
Random Forest
        ↓
Fraud Prediction
        ↓
Risk Level
        ↓
Supabase
```

This will make SecurePay AI closer to a real-world UPI fraud detection system.

---

# 19. Today's Conclusion

Today's major achievement was completing the first working backend integration:

```text
FastAPI
   ↓
Random Forest
   ↓
Fraud Detection
   ↓
Supabase
```

The system can now receive a transaction through an API, run the trained fraud detection model, calculate fraud probability and risk level, and store the prediction in Supabase.

PostgreSQL was replaced with Supabase.

```
```
