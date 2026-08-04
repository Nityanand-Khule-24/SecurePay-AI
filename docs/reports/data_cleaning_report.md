# Data Cleaning Report

## Project Information

| Field | Value |
|--------|-------|
| Project Name | SecurePay AI |
| Phase | Phase 2 – Data Engineering |
| Step | Step 4 – Data Cleaning |
| Dataset | PaySim Financial Transactions Dataset |
| Input File | dataset/raw/paysim.csv |
| Output File | dataset/cleaned/transactions_clean.csv |

---

# Objective

The objective of this phase was to clean and prepare the PaySim dataset for further analysis, feature engineering, machine learning, and real-time streaming. Data cleaning ensures that the dataset is consistent, reliable, and ready for downstream processing.

---

# Cleaning Steps Performed

### 1. Created a Working Copy

A copy of the original dataset was created to preserve the raw data.

**Status:** ✅ Completed

---

### 2. Missing Value Validation

The dataset was checked for missing values across all columns.

**Observation:**

- No missing values were found.

**Action Taken:**

- No imputation was required.

**Status:** ✅ Completed

---

### 3. Duplicate Record Validation

The dataset was checked for duplicate transactions.

**Observation:**

- No duplicate records were found.

**Action Taken:**

- No records were removed.

**Status:** ✅ Completed

---

### 4. Column Name Standardization

Column names were standardized by converting all names to lowercase.

Example:

| Before | After |
|---------|-------|
| oldbalanceOrg | oldbalanceorg |
| newbalanceOrig | newbalanceorig |
| isFraud | isfraud |

**Status:** ✅ Completed

---

### 5. Text Data Cleaning

Whitespace was removed from all object (string) columns to ensure consistency.

**Columns Cleaned**

- type
- nameorig
- namedest

**Status:** ✅ Completed

---

### 6. Transaction Type Validation

The transaction type column was validated.

Valid transaction types identified:

- PAYMENT
- TRANSFER
- CASH_OUT
- CASH_IN
- DEBIT

No invalid transaction types were detected.

**Status:** ✅ Completed

---

### 7. Numeric Data Validation

Numeric columns were inspected for invalid values.

Checks Performed:

- Negative transaction amounts
- Invalid balance values
- Data consistency

**Observation:**

No invalid numeric values requiring correction were identified.

**Status:** ✅ Completed

---

### 8. Data Type Optimization

Numeric columns were converted to more memory-efficient data types.

| Column | Original Type | Optimized Type |
|---------|---------------|----------------|
| step | int64 | int32 |
| amount | float64 | float32 |
| oldbalanceorg | float64 | float32 |
| newbalanceorig | float64 | float32 |
| oldbalancedest | float64 | float32 |
| newbalancedest | float64 | float32 |
| isfraud | int64 | int8 |
| isflaggedfraud | int64 | int8 |

This optimization reduces memory usage while preserving the required precision for analysis.

**Status:** ✅ Completed

---

### 9. Cleaned Dataset Export

The cleaned dataset was exported for use in the next stage of the project.

Output File:

```text
dataset/cleaned/transactions_clean.csv
```

**Status:** ✅ Completed

---

# Cleaning Summary

| Cleaning Task | Status |
|---------------|--------|
| Working Copy Created | ✅ |
| Missing Values Checked | ✅ |
| Duplicate Records Checked | ✅ |
| Column Names Standardized | ✅ |
| Text Columns Cleaned | ✅ |
| Transaction Types Validated | ✅ |
| Numeric Columns Validated | ✅ |
| Data Types Optimized | ✅ |
| Cleaned Dataset Saved | ✅ |

---

# Business Impact

The data cleaning process ensures that the dataset is reliable, consistent, and optimized for downstream processing. A standardized dataset improves the quality of feature engineering, machine learning, real-time transaction processing, and receiver risk analysis within the SecurePay AI platform.

---

# Conclusion

The PaySim dataset has been successfully cleaned and prepared for the next phase of the project. All validation checks passed successfully, no critical data quality issues were identified, and the dataset has been optimized for efficient storage and processing.

The cleaned dataset is now ready for:

- Feature Engineering
- Exploratory Data Analysis (EDA)
- PostgreSQL Data Loading
- Apache Kafka Streaming
- Apache Spark Processing
- Machine Learning Model Development

**Project Status:** ✅ Data Cleaning Completed