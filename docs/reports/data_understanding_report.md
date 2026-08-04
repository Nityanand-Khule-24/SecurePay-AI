## Business Rules
Fraud mainly occurs in TRANSFER and CASH_OUT transactions.
PAYMENT, CASH_IN, and DEBIT transactions have very few or no fraud cases in this dataset.
nameOrig is always the sender.
nameDest is always the receiver.
isFraud is the target variable for the ML model.
isFlaggedFraud is a rule-based indicator and can be compared with the ML model later.
Receiver account history will be used to calculate the Receiver Risk Score in SecurePay AI.