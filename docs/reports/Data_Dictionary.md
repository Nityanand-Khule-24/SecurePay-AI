# Data dictionary Report

## Project

**Project Name:** SecurePay AI

**Phase:** Phase 2 – Data Engineering

**Step:** Step 2 – Data understanding

**Dataset:** PaySim Financial Transactions Dataset

**Date:** _04-08-2026_

| Column         | Description                                                        | Example    |
| -------------- | ------------------------------------------------------------------ | ---------- |
| step           | Time step in the PaySim simulation (approximately 1 hour per step) | 1          |
| type           | Type of transaction                                                | PAYMENT    |
| amount         | Amount transferred                                                 | 5000       |
| nameOrig       | Sender account ID                                                  | C123456789 |
| oldbalanceOrg  | Sender balance before the transaction                              | 100000     |
| newbalanceOrig | Sender balance after the transaction                               | 95000      |
| nameDest       | Receiver account ID                                                | C987654321 |
| oldbalanceDest | Receiver balance before the transaction                            | 200000     |
| newbalanceDest | Receiver balance after the transaction                             | 205000     |
| isFraud        | Fraud label (0 = Normal, 1 = Fraud)                                | 1          |
| isFlaggedFraud | System-generated fraud flag                                        | 0          |

## transaction Types

type
CASH_OUT    2237500
PAYMENT     2151495
CASH_IN     1399284
TRANSFER     532909
DEBIT         41432

| Transaction Type | Description                     | Relevant to UPI?                                      |
| ---------------- | ------------------------------- | ----------------------------------------------------  |
| PAYMENT          | Payment to merchants/services   | ✅ Yes                                               |
| TRANSFER         | Account-to-account transfer     | ✅ Yes                                               |
| CASH_OUT         | Money withdrawn from an account | ⚠️ Similar to cash withdrawal after receiving money  |
| CASH_IN          | Money deposited into an account | ❌ Not common in UPI                                 |
| DEBIT            | Direct debit transaction        | ⚠️ Less common                                       |

## Fraud Distribution

isFraud	0	1
type		
CASH_IN	100.000000	0.000000
CASH_OUT	99.816045	0.183955
DEBIT	100.000000	0.000000
PAYMENT	100.000000	0.000000
TRANSFER	99.231201	0.768799