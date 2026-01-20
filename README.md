# PayPal Payments Data Pipeline

An end-to-end data engineering project that ingests PayPal Checkout Orders, stores raw events in AWS S3, transforms captured payments using Python, and serves analytics-ready data in BigQuery.

---

## 🚀 Architecture Overview

PayPal Checkout Orders API  
→ Raw JSON stored in AWS S3 (data lake)  
→ Python transformation layer  
→ Payments fact CSV  
→ BigQuery analytics  

---

## 🧱 Tech Stack

- **Language:** Python 3
- **APIs:** PayPal Checkout Orders API (Sandbox)
- **Cloud Storage:** AWS S3
- **Data Warehouse:** Google BigQuery (Sandbox)
- **Data Formats:** JSON (raw), CSV (processed)
- **Version Control:** Git + GitHub

---

## 🔄 Pipeline Flow

1. **Ingestion**
   - Fetch PayPal Checkout Orders using OAuth2 authentication
   - Store raw JSON responses in S3 for immutability

2. **Transformation**
   - Parse captured payment details from orders
   - Handle sandbox limitations using schema-accurate mock payloads
   - Generate analytics-ready payments fact CSV

3. **Analytics**
   - Load processed CSV into BigQuery
   - Run SQL queries for payment insights

---

## 📊 Sample Analytics Queries

```sql
SELECT currency, COUNT(*) AS payments, SUM(amount) AS total_amount
FROM paypal_analytics.payments_fact
GROUP BY currency;