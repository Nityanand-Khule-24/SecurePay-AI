# SecurePay AI – Development Progress Report

## Date

12 August 2026

## Project

**SecurePay AI – Real-Time UPI Fraud Detection & Receiver Risk Analysis Platform**

---

# 1. Today's Objective

The main objective today was to connect the SecurePay AI machine learning pipeline with **Supabase** and verify that Python can successfully store transaction data in the database.

Before starting the database integration, the following stages had already been completed:

- Data Loading
- Data Understanding
- Data Cleaning
- Exploratory Data Analysis
- Feature Engineering
- Final ML Model

Today we started the database/backend integration using Supabase instead of PostgreSQL.

---

# 2. Completed Project Stages

Current project progress:

| Stage | Status |
|---|---|
| 01 – Data Loading | ✅ Completed |
| 02 – Data Understanding | ✅ Completed |
| 03 – Data Cleaning | ✅ Completed |
| 04 – Exploratory Data Analysis | ✅ Completed |
| 05 – Feature Engineering | ✅ Completed |
| 06 – Final ML Model | ✅ Completed |
| 07 – Supabase Setup | ✅ Completed |
| 08 – Database Schema | ✅ Completed |
| 09 – Python → Supabase Connection | ✅ Completed |
| 10 – Test Transaction Insert | ✅ Completed |

---

# 3. Supabase Setup

Supabase was selected as the database/backend service instead of PostgreSQL.

The purpose of Supabase in SecurePay AI is to store:

- Transactions
- Fraud predictions
- Receiver risk information

The database will later be connected to the real-time transaction pipeline.

---

# 4. Database Structure

Three main tables were created in Supabase.

## 4.1 transactions

This table stores transaction information.

Important fields include:

- transaction_id
- step
- transaction_type
- amount
- sender_id
- receiver_id
- sender_balance_before
- sender_balance_after
- receiver_balance_before
- receiver_balance_after
- is_fraud
- created_at

---

## 4.2 fraud_predictions

This table will store ML model predictions.

Fields include:

- prediction_id
- transaction_id
- fraud_probability
- prediction
- risk_level
- model_version
- created_at

---

## 4.3 receiver_risk

This table will store receiver-level risk information.

Fields include:

- receiver_id
- transaction_count
- previous_fraud
- historical_fraud_rate
- risk_score
- updated_at

The `receiver_risk` table is particularly important because SecurePay AI focuses on identifying suspicious receivers.

---

# 5. Database Folder Structure

The following database structure was created:

```text
D:\SecurePay-AI\

├── database/
│   ├── connection.py
│   └── test_insert.py
│
├── .env
├── .gitignore
├── dataset/
├── ml/
└── reports/
````

---

# 6. Environment Variables

A `.env` file was created to securely store Supabase credentials.

Example:

```env
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_KEY=YOUR_SECRET_KEY
```

The actual credentials are not stored directly inside Python source code.

---

# 7. Git Security

The `.env` file was added to `.gitignore`.

```text
.env
```

This prevents the Supabase credentials from being uploaded to GitHub.

This is important because the Supabase secret key provides privileged backend access.

---

# 8. Python Supabase Connection

The file:

```text
database/connection.py
```

was created to initialize the Supabase client.

The connection uses:

* Python
* supabase-py
* python-dotenv
* environment variables

The connection was successfully tested.

Output:

```text
URL loaded: True
KEY loaded: True
Supabase connection initialized successfully....
```

This confirms that Python can successfully initialize the Supabase client.

---

# 9. Errors Faced During Supabase Integration

Several errors occurred during the integration process.

## Error 1 – Connection Timeout

Initially, the Supabase request produced:

```text
httpx.ConnectTimeout:
_ssl.c:1063: The handshake operation timed out
```

### What happened?

Python was able to initialize the Supabase client, but the HTTPS/SSL connection to the Supabase API timed out.

### Solution

The connection was tested again and the issue was resolved.

Afterward, Python successfully reached the Supabase API.

---

# 10. Error 2 – Row Level Security

After the connection started working, the insert operation produced:

```text
postgrest.exceptions.APIError:

new row violates row-level security policy
for table "transactions"
```

### Cause

Row Level Security (RLS) was enabled on the `transactions` table.

The existing policy only allowed:

```text
authenticated
```

for INSERT operations.

The Python request was not matching that policy.

---

# 11. RLS Policy Fix

A development INSERT policy for the `anon` role was created:

```sql
CREATE POLICY "Allow anon insert transactions"
ON public.transactions
FOR INSERT
TO anon
WITH CHECK (true);
```

The policies were verified using:

```sql
SELECT
    policyname,
    roles,
    cmd,
    with_check
FROM pg_policies
WHERE tablename = 'transactions';
```

The resulting policies were:

```text
Allow backend insert transactions | {authenticated} | INSERT | true

Allow anon insert transactions    | {anon}          | INSERT | true
```

RLS was confirmed to be enabled:

```text
relrowsecurity = true
relforcerowsecurity = false
```

---

# 12. Error 3 – Environment Variables Not Loaded

At one point Python returned:

```text
URL loaded: False
KEY loaded: False
```

and:

```text
ValueError: Supabase credentials are not set.....
```

### Cause

Python was not finding the `.env` file correctly when executing:

```text
python database\test_insert.py
```

### Solution

The `.env` path was made explicit in `connection.py`.

Python now finds `.env` from the project root:

```text
D:\SecurePay-AI\.env
```

After the fix:

```text
URL loaded: True
KEY loaded: True
```

---

# 13. Test Transaction

A test transaction was created in:

```text
database/test_insert.py
```

The test transaction contained:

```text
step: 1
transaction_type: TRANSFER
amount: 5000.00

sender_id: C_TEST_001
receiver_id: C_TEST_002

sender_balance_before: 10000.00
sender_balance_after: 5000.00

receiver_balance_before: 2000.00
receiver_balance_after: 7000.00

is_fraud: 0
```

---

# 14. Final Successful Test

The final test was executed using:

```powershell
python database\test_insert.py
```

Output:

```text
URL loaded: True
KEY loaded: True
Supabase connection initialized successfully....
transaction inserted successfully
```

Supabase returned the inserted transaction:

```text
transaction_id: 5
step: 1
transaction_type: TRANSFER
amount: 5000.0
sender_id: C_TEST_001
receiver_id: C_TEST_002
sender_balance_before: 10000.0
sender_balance_after: 5000.0
receiver_balance_before: 2000.0
receiver_balance_after: 7000.0
is_fraud: 0
```

This confirms that the transaction was successfully inserted into the Supabase `transactions` table.

---

# 15. Current Architecture

The current working part of the architecture is:

```text
Python
   |
   v
.env
   |
   v
Supabase Client
   |
   v
Supabase API
   |
   v
RLS Policy
   |
   v
transactions Table
```

The complete SecurePay AI architecture will later become:

```text
UPI Transaction
       |
       v
Apache Kafka
       |
       v
Apache Spark Streaming
       |
       v
Data Validation
       |
       v
Feature Engineering
       |
       +--------------------+
       |                    |
       v                    v
Fraud ML Model       Receiver Risk Engine
       |                    |
       +---------+----------+
                 |
                 v
          Decision Engine
                 |
                 v
             Supabase
          /      |       \
         /       |        \
Transactions  Predictions  Receiver Risk
                 |
                 v
          FastAPI Backend
                 |
                 v
        SecurePay AI Frontend
```

---

# 16. Current Status

The following database integration components are working:

```text
Supabase Project             ✅
Database Tables              ✅
RLS Configuration            ✅
.env Configuration           ✅
.gitignore Configuration     ✅
Python Supabase Client       ✅
Python → Supabase Connection ✅
Transaction INSERT           ✅
```

---

# 17. Important Security Note

The `.env` file must never be committed to GitHub.

The secret key should only be used by backend/server-side components.

Before production deployment, RLS policies should be reviewed and tightened according to the final application architecture.

The development policy:

```sql
TO anon
WITH CHECK (true)
```

should not automatically be used as the final production security configuration.

---

# 18. Next Step

The next task is to create a reusable database service layer.

New file:

```text
database/
└── transaction_service.py
```

This file will contain reusable functions such as:

```text
insert_transaction()
get_transaction()
get_recent_transactions()
```

This will prevent the Kafka, Spark, and FastAPI components from directly containing database logic.

After that, the ML prediction results will be connected to:

```text
fraud_predictions
```

and receiver risk information will be connected to:

```text
receiver_risk
```

---

# 19. Today's Final Result

Today we successfully moved SecurePay AI from the **ML development stage** into the **database/backend integration stage**.

The most important milestone was:

```text
Python
   ↓
Supabase
   ↓
transactions
   ↓
✅ Real transaction stored successfully
```

This proves that the SecurePay AI backend can communicate with Supabase and store transaction data successfully.

---

