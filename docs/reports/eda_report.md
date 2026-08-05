# Exploratory Data Analysis (EDA) Report

## Project Information

| Field | Value |
|--------|-------|
| Project Name | SecurePay AI |
| Phase | Phase 2 – Data Engineering |
| Step | Step 5 – Exploratory Data Analysis (EDA) |
| Dataset | PaySim Financial Transactions Dataset |
| Input File | dataset/cleaned/transactions_clean.csv |

---

# Objective

The objective of this Exploratory Data Analysis (EDA) is to understand the characteristics of the PaySim dataset, identify fraud patterns, analyze customer and receiver behavior, and extract business insights that will support feature engineering, machine learning, and the Receiver Risk Engine used in SecurePay AI.

---

# EDA Sections Performed

## 1. Dataset Overview

The cleaned dataset was successfully loaded and verified.

### Analysis Performed

- Dataset shape
- Column information
- Data types
- Basic statistics

### Status

✅ Completed

---

## 2. Target Variable Analysis

### Analysis Performed

- Total normal transactions
- Total fraudulent transactions
- Fraud percentage
- Class imbalance analysis

### Visualizations

- Bar Chart: Normal vs Fraud Transactions
- Pie Chart: Fraud Distribution

### Key Findings

- The dataset is highly imbalanced.
- Fraudulent transactions represent only a very small percentage of all transactions.
- Class imbalance must be considered during machine learning model development.

---

## 3. Transaction Type Analysis

### Analysis Performed

- Frequency of each transaction type
- Fraud percentage by transaction type

### Visualizations

- Transaction Type Bar Chart
- Fraud Percentage by Transaction Type

### Key Findings

- PAYMENT transactions are the most frequent.
- Fraud is concentrated mainly in **TRANSFER** and **CASH_OUT** transaction types.
- Other transaction types contain little or no fraud.

---

## 4. Transaction Amount Analysis

### Analysis Performed

- Average transaction amount
- Median transaction amount
- Minimum transaction amount
- Maximum transaction amount
- Fraud vs Normal amount comparison

### Visualizations

- Histogram
- Box Plot
- Fraud vs Normal Box Plot

### Key Findings

- Transaction amounts vary widely.
- Fraudulent transactions generally involve higher transaction amounts.
- Several extreme-value transactions (outliers) were identified.

---

## 5. Sender Analysis

### Analysis Performed

- Top senders by transaction count
- Top senders by transaction amount
- Fraud analysis by sender

### Visualizations

- Top Sender Transactions
- Top Sender Amounts

### Key Findings

- A small number of senders perform a high number of transactions.
- Sender transaction behavior can be useful for future risk scoring.

---

## 6. Receiver Analysis

### Analysis Performed

- Top receivers by transaction count
- Top receivers by received amount
- Receivers involved in fraudulent transactions
- Receiver fraud frequency

### Visualizations

- Top Receiver Transactions
- Top Receiver Amounts
- Receiver Fraud Count

### Key Findings

- Certain receiver accounts repeatedly appear in fraudulent transactions.
- Receiver history is an important indicator of fraud.
- These findings will be used to develop the Receiver Risk Engine.

---

## 7. Balance Analysis

### Analysis Performed

- Sender balance before transaction
- Sender balance after transaction
- Receiver balance before transaction
- Receiver balance after transaction

### Visualizations

- Histograms
- Box Plots

### Key Findings

- Significant balance changes occur during fraudulent transactions.
- Balance-related features are expected to improve fraud detection accuracy.

---

## 8. Time Analysis

### Analysis Performed

- Transaction volume over time
- Fraud occurrence over time
- Peak transaction periods

### Visualizations

- Transaction Trend Line Chart
- Fraud Trend Line Chart

### Key Findings

- Transaction volume changes across different time steps.
- Fraud occurrences are distributed unevenly throughout the dataset.
- Time-based features may improve model performance.

---

## 9. Correlation Analysis

### Analysis Performed

- Correlation matrix
- Heatmap of numerical features

### Visualizations

- Correlation Matrix
- Heatmap

### Key Findings

- Balance-related features show meaningful relationships.
- Some numerical variables have stronger associations with fraud than others.
- These features will be prioritized during feature engineering.

---

# Business Insights

Based on the exploratory analysis, the following business insights were identified:

- Fraudulent transactions account for only a very small percentage of all transactions, indicating a highly imbalanced dataset.
- Fraud occurs primarily in **TRANSFER** and **CASH_OUT** transaction types.
- Fraudulent transactions generally involve larger transaction amounts than normal transactions.
- Certain receiver accounts repeatedly appear in fraudulent transactions and should receive higher Receiver Risk Scores.
- Transaction history and receiver behavior are important indicators for fraud detection.
- Sender and receiver balance changes provide valuable information for identifying suspicious activity.
- Time-based transaction patterns may improve fraud prediction.
- Correlation analysis identified several numerical features suitable for machine learning.

---

# Impact on SecurePay AI

The findings from this EDA directly support the design of the SecurePay AI platform.

The extracted insights will be used for:

- Receiver Risk Score Calculation
- Feature Engineering
- Machine Learning Model Development
- Fraud Detection Engine
- Real-Time Alert System
- Decision Engine
- FastAPI Backend
- Power BI Dashboard

---

# Conclusion

The Exploratory Data Analysis successfully identified important fraud patterns, transaction behaviors, and receiver characteristics within the PaySim dataset. The analysis provides a strong foundation for building the Receiver Risk Engine and developing an effective fraud detection model.

The cleaned dataset and business insights are now ready for the next phase of the project: **Feature Engineering**.

---

## Project Status

| Phase | Status |
|--------|--------|
| Data Loading | ✅ Completed |
| Data Understanding | ✅ Completed |
| Data Validation | ✅ Completed |
| Data Cleaning | ✅ Completed |
| Exploratory Data Analysis | ✅ Completed |
| Feature Engineering | ⏳ Next Phase |