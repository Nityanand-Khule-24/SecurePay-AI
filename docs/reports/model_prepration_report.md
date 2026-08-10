SecurePay AI — Model Preparation Report

1. Project Information
Item	Details
Project	SecurePay AI
Notebook	05_model_preparation.ipynb
ML Task	Binary fraud classification
Model	Random Forest Classifier
Target	isfraud
Dataset	Feature-engineered PaySim transaction data

2. Objective

The purpose of this notebook is to prepare the feature-engineered transaction data and train an initial machine-learning model for SecurePay AI.

The model classifies transactions into:

0 — Normal transaction
1 — Fraudulent transaction

The resulting model is intended to become the Transaction Risk Engine of SecurePay AI.

3. Input Dataset

The notebook loads:

D:\SecurePay-AI\dataset\feature_engineered\feature_engineered.csv

The displayed dataset contains 27 columns after feature engineering, including transaction, sender, receiver, balance, time, and receiver-risk features.

The notebook also creates sender_total_amount from the sender's transaction history because it was required by the selected feature list.

4. Selected Features

The model uses the following 19 input features:

type
amount
oldbalanceorg
newbalanceorig
oldbalancedest
newbalancedest
large_transaction
sender_transaction_count
sender_total_amount
receiver_transaction_count
receiver_total_amount
receiver_fraud_count
receiver_fraud_rate
sender_balance_change
receiver_balance_change
balance_ratio
hour
night_transaction
receiver_risk_score

The target variable is:

isfraud
5. Data Preprocessing
5.1 Sender Total Amount

The notebook creates:

sender_amount = (
    df.groupby("nameorig")["amount"]
      .sum()
)

df["sender_total_amount"] = (
    df["nameorig"].map(sender_amount)
)

This adds the total transaction amount associated with each sender.

5.2 Categorical Encoding

The type column is categorical, so a LabelEncoder is used:

encoder = LabelEncoder()

X["type"] = encoder.fit_transform(X["type"])

The notebook saves the encoder as:

ml/lable_encoder.pkl

Note: the current artifact name is lable_encoder.pkl (with lable, not label). It is recommended to rename it to label_encoder.pkl later for consistency.

5.3 Train/Test Split

The notebook uses an 80/20 train/test split:

train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

Stratification is enabled to preserve the fraud/normal class distribution between training and testing data.

6. Class Imbalance

The notebook uses:

class_weight = "balanced"

and configures the Random Forest with:

class_weight="balanced"

This is intended to give additional importance to the minority fraud class.

7. Model Configuration

The selected model is:

RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)
Configuration
Parameter	Value
Algorithm	Random Forest
Number of trees	200
Random state	42
Class weighting	Balanced

The model was successfully fitted on the training data.

8. Model Evaluation Results

The notebook reports the following results on the test set:

Metric	Result
Accuracy	99.999607%
Precision	100.000000%
Recall	99.695679%
F1 Score	99.847607%

The test set contains:

1,272,524 transactions
Classification Report
Class	Precision	Recall	F1-score	Support
Normal (0)	1.00	1.00	1.00	1,270,881
Fraud (1)	1.00	1.00	1.00	1,643
Macro Avg	1.00	1.00	1.00	1,272,524
Weighted Avg	1.00	1.00	1.00	1,272,524

The displayed classification report rounds the fraud metrics to 1.00, while the directly calculated recall and F1 values above preserve their full precision.

9. Confusion Matrix

Based on the notebook's reported test-set support and metrics, the confusion matrix corresponds to:

Actual \ Predicted	Normal	Fraud
Normal	1,270,881	0
Fraud	5	1,638
Interpretation
True Negatives: 1,270,881
False Positives: 0
False Negatives: 5
True Positives: 1,638

The model therefore detected 1,638 of the 1,643 fraudulent transactions in the test set and missed 5.

The notebook also generated a confusion-matrix visualization.

10. Feature Importance

The notebook calculates Random Forest feature importance using:

importance = pd.Series(
    rf.feature_importances_,
    index=X.columns
)

importance = importance.sort_values(ascending=False)

A horizontal bar chart titled:

feature importance

was generated.

The notebook output confirms that feature importance analysis was performed. The saved notebook does not provide the numerical feature-importance values as text, so this report does not invent or assign numerical rankings to individual features.

11. Model Performance Interpretation

The initial Random Forest model produced extremely high test-set performance:

Accuracy is approximately 99.9996%.
Precision is 100%, meaning no false-positive predictions were reported on this test set.
Fraud recall is approximately 99.70%, meaning 5 fraudulent transactions were missed.
F1 score is approximately 99.85%.

For a fraud detection system, recall is especially important because false negatives represent fraudulent transactions that were not detected.

12. Important Data Leakage Consideration

The current notebook uses receiver-related features such as:

receiver_fraud_count
receiver_fraud_rate
receiver_risk_score

These features were already calculated in the feature-engineering dataset before the train/test split.

This creates a potential data leakage risk, because receiver fraud statistics may contain information derived from transactions that later appear in the test set.

The extremely high test performance should therefore not yet be treated as the final production performance of SecurePay AI.

For a production-quality model, receiver history should be generated using only information available before the transaction being predicted.

Recommended concept:

Historical Transactions
        |
        v
Build Historical Receiver Profile
        |
        v
Generate Features for Current Transaction
        |
        v
Fraud Model
        |
        v
Prediction

This should be addressed before the final model is deployed.

13. Current Technical Issues Observed
13.1 SettingWithCopyWarning

The notebook produced a Pandas SettingWithCopyWarning while encoding type:

X["type"] = encoder.fit_transform(X["type"])

A safer implementation is:

X = df[features].copy()

X["type"] = encoder.fit_transform(X["type"])

This avoids modifying a view of the original DataFrame.

13.2 Encoder Filename

The notebook currently saves:

lable_encoder.pkl

Recommended filename:

label_encoder.pkl
13.3 Feature Naming

The feature-engineered dataset contains:

sender_transaction_amount

while the ML notebook creates:

sender_total_amount

The project should standardize this naming before the final pipeline is implemented.

14. SecurePay AI Architecture Integration

The trained model will later operate as the Transaction Risk Engine.

UPI Transaction
      |
      v
FastAPI Backend
      |
      +-----------------------+
      |                       |
      v                       v
Receiver Risk Engine    Transaction Risk Engine
      |                       |
      v                       v
Receiver Risk Score     Fraud Prediction
      |                       |
      +-----------+-----------+
                  |
                  v
            Decision Engine
             /           \
            /             \
           v               v
   Safe Transaction     Fraud Alert

The Receiver Risk Engine evaluates the receiver, while the ML model evaluates the transaction itself.

15. Current Deliverables

The notebook currently contains:

Feature selection
Sender total amount feature creation
Categorical encoding
Train/test split
Class imbalance configuration
Random Forest training
Transaction prediction
Accuracy calculation
Precision calculation
Recall calculation
F1-score calculation
Classification report
Confusion matrix visualization
Feature importance calculation
Feature importance visualization
16. Conclusion

The initial SecurePay AI fraud-detection model has been successfully trained using a Random Forest Classifier with 200 trees and balanced class weights.

The model achieved:

Accuracy : 99.999607%
Precision: 100.000000%
Recall   : 99.695679%
F1 Score : 99.847607%

on the notebook's test set of 1,272,524 transactions.

These results are very strong, but they should be treated as initial experimental results, not final production results, because receiver-history features may introduce data leakage.

The next ML task should therefore be to redesign the receiver-history features using time-aware/historical information, retrain the model, and compare the new results with this baseline.

Project Status
Component	Status
Data Loading	Completed
Data Understanding	Completed
Data Validation	Completed
Data Cleaning	Completed
EDA	Completed
Feature Engineering	Completed
Receiver Risk Engine	Completed
Initial ML Model	Completed
Leakage Review	Required
Final ML Model	Pending
PostgreSQL	Pending
FastAPI Backend	Pending
Kafka	Pending
Spark Streaming	Pending
React Frontend	Pending
Docker Deployment	Pending
model_preparation_report.md
SecurePay AI — Model Preparation Report
1. Project Information
Item	Details
Project	SecurePay AI
Notebook	05_model_preparation.ipynb
ML Task	Binary fraud classification
Model	Random Forest Classifier
Target	isfraud
Dataset	Feature-engineered PaySim transaction data
2. Objective

The purpose of this notebook is to prepare the feature-engineered transaction data and train an initial machine-learning model for SecurePay AI.

The model classifies transactions into:

0 — Normal transaction
1 — Fraudulent transaction

The resulting model is intended to become the Transaction Risk Engine of SecurePay AI.

3. Input Dataset

The notebook loads:

D:\SecurePay-AI\dataset\feature_engineered\feature_engineered.csv

The displayed dataset contains 27 columns after feature engineering, including transaction, sender, receiver, balance, time, and receiver-risk features.

The notebook also creates sender_total_amount from the sender's transaction history because it was required by the selected feature list.

4. Selected Features

The model uses the following 19 input features:

type
amount
oldbalanceorg
newbalanceorig
oldbalancedest
newbalancedest
large_transaction
sender_transaction_count
sender_total_amount
receiver_transaction_count
receiver_total_amount
receiver_fraud_count
receiver_fraud_rate
sender_balance_change
receiver_balance_change
balance_ratio
hour
night_transaction
receiver_risk_score

The target variable is:

isfraud
5. Data Preprocessing
5.1 Sender Total Amount

The notebook creates:

sender_amount = (
    df.groupby("nameorig")["amount"]
      .sum()
)

df["sender_total_amount"] = (
    df["nameorig"].map(sender_amount)
)

This adds the total transaction amount associated with each sender.

5.2 Categorical Encoding

The type column is categorical, so a LabelEncoder is used:

encoder = LabelEncoder()

X["type"] = encoder.fit_transform(X["type"])

The notebook saves the encoder as:

ml/lable_encoder.pkl

Note: the current artifact name is lable_encoder.pkl (with lable, not label). It is recommended to rename it to label_encoder.pkl later for consistency.

5.3 Train/Test Split

The notebook uses an 80/20 train/test split:

train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

Stratification is enabled to preserve the fraud/normal class distribution between training and testing data.

6. Class Imbalance

The notebook uses:

class_weight = "balanced"

and configures the Random Forest with:

class_weight="balanced"

This is intended to give additional importance to the minority fraud class.

7. Model Configuration

The selected model is:

RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)
Configuration
Parameter	Value
Algorithm	Random Forest
Number of trees	200
Random state	42
Class weighting	Balanced

The model was successfully fitted on the training data.

8. Model Evaluation Results

The notebook reports the following results on the test set:

Metric	Result
Accuracy	99.999607%
Precision	100.000000%
Recall	99.695679%
F1 Score	99.847607%

The test set contains:

1,272,524 transactions
Classification Report
Class	Precision	Recall	F1-score	Support
Normal (0)	1.00	1.00	1.00	1,270,881
Fraud (1)	1.00	1.00	1.00	1,643
Macro Avg	1.00	1.00	1.00	1,272,524
Weighted Avg	1.00	1.00	1.00	1,272,524

The displayed classification report rounds the fraud metrics to 1.00, while the directly calculated recall and F1 values above preserve their full precision.

9. Confusion Matrix

Based on the notebook's reported test-set support and metrics, the confusion matrix corresponds to:

Actual \ Predicted	Normal	Fraud
Normal	1,270,881	0
Fraud	5	1,638
Interpretation
True Negatives: 1,270,881
False Positives: 0
False Negatives: 5
True Positives: 1,638

The model therefore detected 1,638 of the 1,643 fraudulent transactions in the test set and missed 5.

The notebook also generated a confusion-matrix visualization.

10. Feature Importance

The notebook calculates Random Forest feature importance using:

importance = pd.Series(
    rf.feature_importances_,
    index=X.columns
)

importance = importance.sort_values(ascending=False)

A horizontal bar chart titled:

feature importance

was generated.

The notebook output confirms that feature importance analysis was performed. The saved notebook does not provide the numerical feature-importance values as text, so this report does not invent or assign numerical rankings to individual features.

11. Model Performance Interpretation

The initial Random Forest model produced extremely high test-set performance:

Accuracy is approximately 99.9996%.
Precision is 100%, meaning no false-positive predictions were reported on this test set.
Fraud recall is approximately 99.70%, meaning 5 fraudulent transactions were missed.
F1 score is approximately 99.85%.

For a fraud detection system, recall is especially important because false negatives represent fraudulent transactions that were not detected.

12. Important Data Leakage Consideration

The current notebook uses receiver-related features such as:

receiver_fraud_count
receiver_fraud_rate
receiver_risk_score

These features were already calculated in the feature-engineering dataset before the train/test split.

This creates a potential data leakage risk, because receiver fraud statistics may contain information derived from transactions that later appear in the test set.

The extremely high test performance should therefore not yet be treated as the final production performance of SecurePay AI.

For a production-quality model, receiver history should be generated using only information available before the transaction being predicted.

Recommended concept:

Historical Transactions
        |
        v
Build Historical Receiver Profile
        |
        v
Generate Features for Current Transaction
        |
        v
Fraud Model
        |
        v
Prediction

This should be addressed before the final model is deployed.

13. Current Technical Issues Observed
13.1 SettingWithCopyWarning

The notebook produced a Pandas SettingWithCopyWarning while encoding type:

X["type"] = encoder.fit_transform(X["type"])

A safer implementation is:

X = df[features].copy()

X["type"] = encoder.fit_transform(X["type"])

This avoids modifying a view of the original DataFrame.

13.2 Encoder Filename

The notebook currently saves:

lable_encoder.pkl

Recommended filename:

label_encoder.pkl
13.3 Feature Naming

The feature-engineered dataset contains:

sender_transaction_amount

while the ML notebook creates:

sender_total_amount

The project should standardize this naming before the final pipeline is implemented.

14. SecurePay AI Architecture Integration

The trained model will later operate as the Transaction Risk Engine.

UPI Transaction
      |
      v
FastAPI Backend
      |
      +-----------------------+
      |                       |
      v                       v
Receiver Risk Engine    Transaction Risk Engine
      |                       |
      v                       v
Receiver Risk Score     Fraud Prediction
      |                       |
      +-----------+-----------+
                  |
                  v
            Decision Engine
             /           \
            /             \
           v               v
   Safe Transaction     Fraud Alert

The Receiver Risk Engine evaluates the receiver, while the ML model evaluates the transaction itself.

15. Current Deliverables

The notebook currently contains:

Feature selection
Sender total amount feature creation
Categorical encoding
Train/test split
Class imbalance configuration
Random Forest training
Transaction prediction
Accuracy calculation
Precision calculation
Recall calculation
F1-score calculation
Classification report
Confusion matrix visualization
Feature importance calculation
Feature importance visualization
16. Conclusion

The initial SecurePay AI fraud-detection model has been successfully trained using a Random Forest Classifier with 200 trees and balanced class weights.

The model achieved:

Accuracy : 99.999607%
Precision: 100.000000%
Recall   : 99.695679%
F1 Score : 99.847607%

on the notebook's test set of 1,272,524 transactions.

These results are very strong, but they should be treated as initial experimental results, not final production results, because receiver-history features may introduce data leakage.

The next ML task should therefore be to redesign the receiver-history features using time-aware/historical information, retrain the model, and compare the new results with this baseline.

Project Status
Component	Status
Data Loading	Completed
Data Understanding	Completed
Data Validation	Completed
Data Cleaning	Completed
EDA	Completed
Feature Engineering	Completed
Receiver Risk Engine	Completed
Initial ML Model	Completed
Leakage Review	Required
Final ML Model	Pending
PostgreSQL	Pending
FastAPI Backend	Pending
Kafka	Pending
Spark Streaming	Pending
React Frontend	Pending
Docker Deployment	Pending