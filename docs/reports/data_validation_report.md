# Data Validation Report

## Project Information

| Field | Value |
|--------|-------|
| Project Name | SecurePay AI |
| Phase | Phase 2 - Data Engineering |
| Step | Step 3 - Data Validation |
| Dataset | PaySim Financial Transactions Dataset |
| Total Records | 6,362,620 |
| Total Columns | 11 |

---

# Validation Summary

| Validation Check | Status | Remarks |
|------------------|--------|---------|
| Missing Values | ✅ Passed | No missing values found |
| Duplicate Records | ✅ Passed | No duplicate records found |
| Data Types | ✅ Passed | All columns have valid data types |
| Transaction Types | ✅ Passed | Five valid transaction types found |
| Fraud Labels | ✅ Passed | Target variable contains only 0 and 1 |
| Fraud Flag | ✅ Passed | isFlaggedFraud contains only 0 and 1 |
| Account IDs | ✅ Passed | Sender IDs begin with 'C', Receiver IDs begin with 'C' or 'M' |
| Numeric Validation | ✅ Passed | No invalid negative balances detected |
| Amount Validation | ✅ Passed | Zero-value fraud records retained for business reasons |

---

# Missing Values

Result:

- No missing values were detected in any column.

Status:

✅ Passed

---

# Duplicate Records

Result:

- No duplicate transactions were found.

Status:

✅ Passed

---

# Data Types Validation

| Column | Data Type |
|----------|-----------|
| step | int64 |
| type | object |
| amount | float64 |
| nameOrig | object |
| oldbalanceOrg | float64 |
| newbalanceOrig | float64 |
| nameDest | object |
| oldbalanceDest | float64 |
| newbalanceDest | float64 |
| isFraud | int64 |
| isFlaggedFraud | int64 |

Status:

✅ All data types are correct.

---

# Unique Values Analysis

| Attribute | Count |
|------------|------:|
| Unique Senders |  6353307 |
| Unique Receivers | 2722362 |
| Transaction Types | 5 |

Transaction Types:

- PAYMENT
- TRANSFER
- CASH_OUT
- CASH_IN
- DEBIT

---

# Fraud Label Validation

Fraud Labels:

| Label | Meaning |
|-------|---------|
| 0 | Normal Transaction |
| 1 | Fraudulent Transaction |

Status:

✅ Target variable validated successfully.

---

# Fraud Flag Validation

isFlaggedFraud contains only:

- 0
- 1

Status:

✅ Passed

---

# Transaction Amount Validation

The transaction amount column was checked for values less than or equal to zero.

Observation:

- A small number of transactions have an amount of 0.0.
- These transactions are labelled as fraudulent.

Business Decision:

These records are intentionally retained because they represent fraud scenarios within the PaySim simulation. Removing them would reduce valuable fraud examples and negatively affect model training.

Status:

✅ Retained

---

# Account ID Validation

Sender Account IDs

- All sender IDs begin with the prefix **C** (Customer).

Receiver Account IDs

- Receiver IDs begin with either:
  - **C** (Customer)
  - **M** (Merchant)

This structure is consistent with the PaySim dataset specification.

Status:

✅ Passed

---

# Validation Conclusion

The PaySim dataset successfully passed all data validation checks. No missing values, duplicate records, or invalid data types were identified. The dataset follows the expected schema, and the account identifiers conform to the PaySim specification. Zero-amount fraudulent transactions were retained because they represent valid fraud scenarios within the simulation and are important for training the fraud detection model.

The dataset is validated and approved for the next phase: **Data Cleaning**.