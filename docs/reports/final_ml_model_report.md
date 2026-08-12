# SecurePay AI — Final Machine Learning Model Report

## Notebook

**Notebook:** `06_final_ml_model.ipynb`

**Project:** SecurePay AI — Enterprise Real-Time UPI Fraud Detection & Analytics Platform

**Dataset:** PaySim

**Model:** Random Forest Classifier

---

# 1. Objective

The objective of this notebook is to prepare and train the final fraud detection machine learning model for SecurePay AI.

The model is designed to identify whether a transaction is:

- Normal
- Fraudulent

The final model uses transaction, sender, receiver, balance, historical behavior, and time-based features.

A major focus of this stage was preventing **data leakage** by ensuring that historical features only use information available before the current transaction.

---

# 2. Dataset

The project uses the PaySim transaction dataset.

The dataset contains simulated financial transactions and includes information about:

- Transaction type
- Transaction amount
- Sender
- Receiver
- Sender balances
- Receiver balances
- Transaction time
- Fraud label

The original dataset is stored locally and is intentionally kept outside GitHub because of its large size.

Example local path:

```text
D:\SecurePay-AI\dataset\raw\paysim.csv
````

The dataset is approximately:

```text
470+ MB
```

The dataset is not uploaded to the GitHub repository.

---

# 3. Data Leakage Consideration

During model preparation, special attention was given to data leakage.

A fraud detection system should only use information that would have been available at the time a transaction occurred.

For example, when predicting transaction `T3`, the model should not use the fraud result of `T3` itself.

Instead, it can use information from:

```text
T1 → T2 → T3
```

For transaction `T3`, only information from `T1` and `T2` should be used for historical features.

This is particularly important for the SecurePay AI receiver risk score.

---

# 4. Historical Receiver Features

Receiver behavior is one of the most important parts of SecurePay AI.

The following historical receiver features were created.

## 4.1 Receiver Transaction Count

This feature counts the number of previous transactions associated with a receiver.

```python
df["receiver_transaction_count"] = (
    df.groupby("namedest")
      .cumcount()
)
```

The first transaction for a receiver has:

```text
receiver_transaction_count = 0
```

The second transaction has:

```text
receiver_transaction_count = 1
```

The third transaction has:

```text
receiver_transaction_count = 2
```

This allows the model to understand receiver transaction frequency.

---

# 5. Previous Receiver Fraud

The number of fraudulent transactions previously associated with the receiver was calculated.

```python
df["previous_receiver_fraud"] = (
    df.groupby("namedest")["isfraud"]
      .transform(
          lambda x: x.shift(1).fillna(0).cumsum()
      )
)
```

The use of:

```python
shift(1)
```

ensures that the current transaction's fraud label is not included.

This prevents target leakage.

---

# 6. Historical Receiver Fraud Rate

The historical receiver fraud rate was calculated using previous receiver transactions.

```python
df["historical_receiver_fraud_rate"] = np.where(
    df["receiver_transaction_count"] > 0,
    df["previous_receiver_fraud"] /
    df["receiver_transaction_count"],
    0
)
```

This feature represents the historical fraud behavior of a receiver.

A receiver with a higher historical fraud rate can receive a higher risk score.

---

# 7. Previous Receiver Amount

The total amount previously received by the receiver was calculated.

```python
df["previous_receiver_amount"] = (
    df.groupby("namedest")["amount"]
      .transform(
          lambda x: x.shift(1).fillna(0).cumsum()
      )
)
```

This feature measures the receiver's historical transaction volume.

---

# 8. Historical Sender Features

Sender behavior was also included in the feature engineering process.

## 8.1 Sender Transaction Count

```python
df["sender_transaction_count"] = (
    df.groupby("nameorig")
      .cumcount()
)
```

This counts previous transactions associated with the sender.

---

## 8.2 Previous Sender Amount

The historical amount associated with the sender was calculated using:

```python
df["previous_sender_amount"] = (
    df.groupby("nameorig")["amount"]
      .transform(
          lambda x: x.shift(1).fillna(0).cumsum()
      )
)
```

This ensures that only previous transactions contribute to the historical amount.

---

# 9. Balance Features

Balance behavior can provide useful information for fraud detection.

## 9.1 Sender Balance Change

```python
df["sender_balance_change"] = (
    df["oldbalanceorg"] -
    df["newbalanceorig"]
)
```

This measures the change in the sender's balance.

---

## 9.2 Receiver Balance Change

```python
df["receiver_balance_change"] = (
    df["newbalancedest"] -
    df["oldbalancedest"]
)
```

This measures the change in the receiver's balance.

---

# 10. Balance Ratio

A balance ratio was created to compare the transaction amount with the sender's previous balance.

```python
df["balance_ratio"] = (
    df["amount"] /
    (df["oldbalanceorg"] + 1)
)
```

The `+1` prevents division by zero.

---

# 11. Time Features

PaySim contains a `step` column representing transaction time.

Two additional time features were created.

## 11.1 Hour

```python
df["hour"] = df["step"] % 24
```

---

## 11.2 Day

```python
df["day"] = df["step"] // 24
```

---

## 11.3 Night Transaction

Transactions occurring between hour 0 and hour 5 were marked as night transactions.

```python
df["night_transaction"] = (
    df["hour"].between(0, 5)
).astype(int)
```

Where:

```text
0 = Not a night transaction
1 = Night transaction
```

---

# 12. Large Transaction Feature

A binary feature was created for large transactions.

```python
df["large_transaction"] = (
    df["amount"] > 100000
).astype(int)
```

Where:

```text
0 = Normal-sized transaction
1 = Large transaction
```

---

# 13. Historical Receiver Risk Score

The receiver risk score is an important component of SecurePay AI.

Three historical receiver signals were combined:

1. Historical receiver fraud rate
2. Receiver transaction frequency
3. Historical receiver transaction amount

Receiver transaction score:

```python
df["receiver_transaction_score"] = (
    df["receiver_transaction_count"] /
    df["receiver_transaction_count"].max()
)
```

Receiver amount score:

```python
df["receiver_amount_score"] = (
    df["previous_receiver_amount"] /
    df["previous_receiver_amount"].max()
)
```

Historical receiver risk score:

```python
df["historical_receiver_risk_score"] = (
      df["historical_receiver_fraud_rate"] * 60
    + df["receiver_transaction_score"] * 20
    + df["receiver_amount_score"] * 20
)
```

The resulting score was rounded:

```python
df["historical_receiver_risk_score"] = (
    df["historical_receiver_risk_score"].round(2)
)
```

This feature will later contribute to the SecurePay AI receiver risk engine.

---

# 14. Final Feature Selection

The following features were selected for the final model:

```python
features = [
    "type",
    "amount",
    "oldbalanceorg",
    "newbalanceorig",
    "oldbalancedest",
    "newbalancedest",
    "large_transaction",

    "sender_transaction_count",
    "previous_sender_amount",

    "receiver_transaction_count",
    "previous_receiver_amount",
    "previous_receiver_fraud",
    "historical_receiver_fraud_rate",

    "sender_balance_change",
    "receiver_balance_change",
    "balance_ratio",

    "hour",
    "night_transaction",

    "historical_receiver_risk_score"
]
```

A total of:

```text
20 features
```

were selected.

---

# 15. Creating X and y

The input features were separated from the target variable.

```python
X = df[features].copy()

y = df["isfraud"].copy()
```

Where:

```text
X = Model input features

y = Fraud target
```

The target column is:

```text
isfraud
```

---

# 16. Encoding Transaction Type

The `type` column is categorical.

A `LabelEncoder` was used.

```python
from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()

X["type"] = encoder.fit_transform(X["type"])
```

The transaction types include:

```text
CASH_IN
CASH_OUT
DEBIT
PAYMENT
TRANSFER
```

The encoder converts these categorical values into numerical values that can be used by the machine learning model.

---

# 17. Time-Aware Train/Test Split

Instead of randomly splitting the dataset, a time-aware split was used.

The first 80% of transactions were used for training.

The final 20% were used for testing.

```python
split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index].copy()
X_test = X.iloc[split_index:].copy()

y_train = y.iloc[:split_index].copy()
y_test = y.iloc[split_index:].copy()
```

This approach is more appropriate for a real-time fraud detection system.

The concept is:

```text
Historical Transactions
        ↓
    Training
        ↓
Future Transactions
        ↓
     Testing
```

This better represents the real-world situation where a fraud model is trained on historical data and then used to predict future transactions.

---

# 18. Random Forest Model

The final machine learning model used was Random Forest.

```python
from sklearn.ensemble import RandomForestClassifier

rf_final = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)
```

## Parameters

| Parameter      |    Value | Purpose                  |
| -------------- | -------: | ------------------------ |
| `n_estimators` |      200 | Number of decision trees |
| `random_state` |       42 | Reproducible results     |
| `class_weight` | balanced | Handles class imbalance  |
| `n_jobs`       |       -1 | Uses available CPU cores |

---

# 19. Model Training

The model was trained using the training dataset.

```python
rf_final.fit(X_train, y_train)
```

---

# 20. Fraud Prediction

Predictions were generated using:

```python
y_pred = rf_final.predict(X_test)
```

Fraud probabilities were also generated:

```python
y_prob = rf_final.predict_proba(X_test)[:, 1]
```

The probability output can later be used as part of the SecurePay AI transaction risk engine.

For example:

```text
Low probability  → Lower risk
Medium probability → Review / warning
High probability → Suspicious transaction
```

The exact production thresholds will be determined later through validation and business requirements.

---

# 21. Final Model Results

The final Random Forest model achieved the following results:

| Metric    |     Result |
| --------- | ---------: |
| Accuracy  | 99.999607% |
| Precision |       100% |
| Recall    | 99.882464% |
| F1 Score  | 99.941197% |

The raw metric values were:

```text
Accuracy  : 0.9999960708010223
Precision : 1.0
Recall    : 0.9988246356370475
F1 Score  : 0.9994119722450899
```

---

# 22. Accuracy

The final model achieved:

```text
99.999607% Accuracy
```

This represents the proportion of correctly classified transactions in the test set.

However, accuracy alone is not sufficient for fraud detection because fraud datasets are highly imbalanced.

---

# 23. Precision

The model achieved:

```text
100% Precision
```

Precision measures how many transactions predicted as fraud were actually fraudulent.

A high precision is important because false fraud alerts can negatively affect legitimate users.

---

# 24. Recall

The model achieved:

```text
99.882464% Recall
```

Recall is especially important for SecurePay AI because it measures how many actual fraudulent transactions were detected.

A high recall means the model is missing very few fraudulent transactions.

---

# 25. F1 Score

The model achieved:

```text
99.941197% F1 Score
```

F1 Score combines precision and recall into a single metric.

Because fraud detection requires both:

```text
High precision
+
High recall
```

F1 Score is an important evaluation metric for this project.

---

# 26. Confusion Matrix

A confusion matrix was generated to analyze:

```text
True Negative
False Positive
False Negative
True Positive
```

Code:

```python
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred)

print(cm)
```

A visualization was also created using Matplotlib.

The confusion matrix helps identify whether the model is:

* Correctly identifying normal transactions
* Correctly identifying fraud
* Generating false fraud alerts
* Missing fraudulent transactions

---

# 27. Feature Importance

Random Forest provides feature importance values.

The following code was used:

```python
importance = pd.DataFrame({
    "feature": X_train.columns,
    "importance": rf_final.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)
```

The top features were visualized using a bar chart.

This analysis is useful for understanding which transaction characteristics contribute most to the model's fraud predictions.

It is also useful for the future SecurePay AI explainability layer.

---

# 28. Model Artifacts

The final machine learning artifacts were stored in:

```text
D:\SecurePay-AI\ml\models\
```

The following files were created:

```text
fraud_model.pkl
label_encoder.pkl
feature_columns.pkl
```

## fraud_model.pkl

Contains the trained Random Forest model.

## label_encoder.pkl

Contains the transaction-type encoder.

## feature_columns.pkl

Contains the exact feature order used during model training.

Keeping the feature order is important because the production system must provide features to the model in the same order used during training.

---

# 29. Errors Encountered and Solutions

During development, several errors occurred. These were resolved before completing the final model.

---

## Error 1 — `receiver_transaction_count` KeyError

### Error

```text
KeyError: 'receiver_transaction_count'
```

### Cause

The column had previously been created with a spelling mistake:

```text
receiver_trnsaction_count
```

instead of:

```text
receiver_transaction_count
```

### Solution

The column was renamed:

```python
df.rename(
    columns={
        "receiver_trnsaction_count":
        "receiver_transaction_count"
    },
    inplace=True
)
```

After that, the correct column name was used throughout the notebook.

---

# 30. Error 2 — Incorrect `previous_sender_amount`

### Problem

The output contained:

```text
<bound method Series.cumsum ...>
```

instead of numerical values.

### Cause

The `cumsum` method was referenced incorrectly.

### Solution

The feature was recreated using:

```python
df["previous_sender_amount"] = (
    df.groupby("nameorig")["amount"]
      .transform(
          lambda x: x.shift(1).fillna(0).cumsum()
      )
)
```

The important part is:

```python
.cumsum()
```

The parentheses execute the method.

---

# 31. Error 3 — `y.name` AttributeError

### Error

```text
AttributeError:
'DataFrame' object has no attribute 'name'
```

### Cause

`y` had accidentally become a DataFrame instead of a Pandas Series.

### Solution

`y` was recreated correctly:

```python
y = df["isfraud"].copy()
```

Then:

```python
print(y.name)
```

worked correctly.

Expected:

```text
isfraud
```

---

# 32. Error 4 — `encoder` NameError

### Error

```text
NameError:
name 'encoder' is not defined
```

### Cause

The `LabelEncoder` object had not been created in the current notebook session.

### Solution

The encoder was imported and instantiated:

```python
from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()
```

Then:

```python
X["type"] = encoder.fit_transform(X["type"])
```

was executed.

---

# 33. Error 5 — `X` NameError

### Error

```text
NameError:
name 'X' is not defined
```

### Cause

The `X` DataFrame had not been created before attempting to encode the transaction type.

### Solution

`X` and `y` were created first:

```python
X = df[features].copy()

y = df["isfraud"].copy()
```

Then the encoder was applied.

Correct sequence:

```text
df
 ↓
features
 ↓
X and y
 ↓
encoder
 ↓
encode type
 ↓
train/test split
```

---

# 34. Error 6 — `LabelEncoder.fit_transform()` TypeError

### Error

```text
TypeError:
LabelEncoder.fit_transform()
missing 1 required positional argument: 'y'
```

### Cause

The `encoder` variable had been incorrectly assigned or was not a proper `LabelEncoder` instance.

### Solution

A fresh encoder object was created:

```python
from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()
```

Then:

```python
X["type"] = encoder.fit_transform(X["type"])
```

The encoder type was verified:

```python
print(type(encoder))
```

Expected:

```text
<class 'sklearn.preprocessing._label.LabelEncoder'>
```

---

# 35. Error 7 — `joblib` NameError

### Error

```text
NameError:
name 'joblib' is not defined
```

### Cause

The `joblib` library had not been imported.

### Solution

```python
import joblib
```

After importing it, the model could be saved using:

```python
joblib.dump(
    rf_final,
    r"D:\SecurePay-AI\ml\models\fraud_model.pkl"
)
```

---

# 36. Error 8 — `rf_final` NameError

### Error

```text
NameError:
name 'rf_final' is not defined
```

### Cause

The Random Forest object did not exist in the current notebook session.

This can happen when:

* The notebook kernel is restarted
* The model creation cell was not executed
* Cells are executed out of order

### Solution

The model was recreated:

```python
rf_final = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)
```

Then trained:

```python
rf_final.fit(X_train, y_train)
```

After training, the model was saved successfully.

---

# 37. Error Prevention Strategy

To avoid these problems in future notebook sessions, cells should be executed in dependency order.

Recommended order:

```text
1. Import libraries
        ↓
2. Load dataset
        ↓
3. Data cleaning
        ↓
4. Sort transactions
        ↓
5. Feature engineering
        ↓
6. Define features
        ↓
7. Create X and y
        ↓
8. Encode categorical features
        ↓
9. Train/test split
        ↓
10. Create model
        ↓
11. Train model
        ↓
12. Evaluate model
        ↓
13. Save model artifacts
```

If the kernel is restarted, cells must be rerun in this order.

---

# 38. Final ML Pipeline

The completed machine learning pipeline is:

```text
PaySim Dataset
      ↓
Data Cleaning
      ↓
Data Understanding
      ↓
EDA
      ↓
Feature Engineering
      ↓
Historical Sender Features
      ↓
Historical Receiver Features
      ↓
Balance Features
      ↓
Time Features
      ↓
Receiver Risk Score
      ↓
Feature Selection
      ↓
Categorical Encoding
      ↓
Time-Aware Train/Test Split
      ↓
Random Forest
      ↓
Fraud Prediction
      ↓
Risk Probability
      ↓
Model Evaluation
      ↓
fraud_model.pkl
```

---

# 39. SecurePay AI Integration

The trained model will later become part of the SecurePay AI fraud detection architecture.

The expected production flow is:

```text
UPI Transaction
      ↓
FastAPI Backend
      ↓
Transaction Validation
      ↓
Feature Generation
      ↓
Receiver Risk Engine
      ↓
Transaction Risk Engine
      ↓
Random Forest Model
      ↓
Fraud Probability
      ↓
Decision Engine
      ↓
┌─────────────────────────┐
│                         │
Safe Transaction     Suspicious Transaction
│                         │
↓                         ↓
Allow Payment          Alert User
```

The receiver risk score will help identify suspicious receivers, while the ML model will evaluate the transaction as a whole.

---

# 40. Important Model Limitation

Although the final model achieved extremely high evaluation scores, these results should not automatically be considered production-level performance.

The project currently uses the PaySim simulated dataset.

Therefore, the model should eventually be tested using:

* Additional datasets
* More realistic transaction distributions
* Real-time streaming transactions
* New unseen receiver behavior
* Changing fraud patterns
* False-positive analysis
* Threshold tuning

Future validation is necessary before making claims about real-world UPI fraud detection performance.

---

# 41. Final Status

The final machine learning stage is completed.

### Completed

* Data preparation
* Historical receiver features
* Historical sender features
* Balance features
* Time features
* Receiver risk score
* Feature selection
* Categorical encoding
* Time-aware train/test split
* Random Forest training
* Fraud prediction
* Model evaluation
* Confusion matrix
* Feature importance
* Model artifact creation

### Final Model

```text
Algorithm: Random Forest Classifier
Trees: 200
Class Weight: Balanced
Random State: 42
```

### Final Results

```text
Accuracy  : 99.999607%
Precision : 100%
Recall    : 99.882464%
F1 Score  : 99.941197%
```

### Model Files

```text
ml/
└── models/
    ├── fraud_model.pkl
    ├── label_encoder.pkl
    └── feature_columns.pkl
```

---

# 42. Next Phase

The next major phase is to integrate the trained ML model with the SecurePay AI data engineering architecture.

The planned components are:

```text
Transaction Simulator
        ↓
Apache Kafka
        ↓
Apache Spark Structured Streaming
        ↓
Data Validation
        ↓
Feature Engineering
        ↓
Fraud Model
        ↓
Risk Score
        ↓
Decision Engine
        ↓
PostgreSQL / BigQuery
        ↓
FastAPI
        ↓
Dashboard / Alert
```

The machine learning model is now ready to become part of the **real-time fraud detection pipeline**.

````