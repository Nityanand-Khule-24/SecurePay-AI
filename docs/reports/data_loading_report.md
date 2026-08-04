# Data Loading Report

## Project

**Project Name:** SecurePay AI

**Phase:** Phase 2 – Data Engineering

**Step:** Step 1 – Data Loading

**Dataset:** PaySim Financial Transactions Dataset

**Date:** _03-08-2026_

---

# Dataset Overview

| Attribute         | Value     |
|-------------------|-----------|
| Number of Rows    | 6,362,620 |
| Number of Columns | 11        |
| Dataset Format    | CSV       |
| File Name         | paysim.csv|
| Target Variable   | isFraud   |

---

# Dataset Size

| Metric       | Value    |
|--------------|----------|
| Memory Usage | 534.0 MB |

---

# Column Information

| Column Name     | Data Type |
|-----------------|-----------|
| step            | int64     |
| type            | object    |
| amount          | float64   |
| nameOrig        | object    |
| oldbalanceOrg   | float64   |
| newbalanceOrig  | float64   |
| nameDest        | object    |
| oldbalanceDest  | float64   |
| newbalanceDest  | float64   |
| isFraud         | int64     |
| isFlaggedFraud  | int64     |

---

# Dataset Structure

Total Columns: **11**

1. step
2. type
3. amount
4. nameOrig
5. oldbalanceOrg
6. newbalanceOrig
7. nameDest
8. oldbalanceDest
9. newbalanceDest
10. isFraud
11. isFlaggedFraud

---

# Data Loading Status

| Check                                  | Status |
|----------------------------------------|--------|
| Dataset Loaded Successfully            | ✅     |
| CSV File Read Successfully             | ✅     |
| Columns Verified                       | ✅     |
| Data Types Verified                    | ✅     |
| Dataset Ready for Data Understanding   | ✅     |

---

# Summary

The PaySim dataset was successfully loaded into a Pandas DataFrame. The dataset contains **6,362,620 transaction records** and **11 columns** representing transaction details, account balances, transaction types, and fraud labels. Initial inspection confirmed that the dataset structure is valid and ready for the next phase, **Data Understanding**, where the business meaning of each attribute and the fraud patterns will be analyzed.


