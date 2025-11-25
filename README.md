# 📊 Vendor Performance Analysis (Power BI + PostgreSQL + Python)

> End-to-end project that cleans raw procurement data using **Python**, loads it into **PostgreSQL**, and builds an interactive **Vendor Performance Dashboard** in **Power BI**.
>
> **Interactive Dashboard Link:** [https://app.powerbi.com/view?r=eyJrIjoiODE3NjNhM2ItZTdiZS00NTUzLWI4NmItY2VmY2VmY2IyMTQ1IiwidCI6IjkxYjYwMzQ5LWFjNmItNDM1NS1hMTc1LWJmNzc5MDhmYmVjMiJ9](https://app.powerbi.com/view?r=eyJrIjoiODE3NjNhM2ItZTdiZS00NTUzLWI4NmItY2VmY2VmY2IyMTQ1IiwidCI6IjkxYjYwMzQ5LWFjNmItNDM1NS1hMTc1LWJmNzc5MDhmYmVjMiJ9)
> 👉 Users can click filters, explore visuals, and interact with the dashboard.

---

## 🚀 Features

> * **Python ETL** to clean, standardize, and load CSVs
> * **PostgreSQL** relational schema (vendors, purchase\_orders, deliveries, invoices, po\_line\_items)
> * **Power BI dashboard** with Key Performance Indicators (KPIs)
> * **Run Sample Analysis Queries** to test the loaded data

---

## ⚙️ Setup and Execution

### PostgreSQL Setup:

> 1.  **[Create DB + User]**
>     ```sql
>     CREATE ROLE vendor_user WITH LOGIN PASSWORD 'your_secure_password';
>     CREATE DATABASE vendor_db OWNER vendor_user;
>     ```
> 2.  **[Run Table Schema]**
>     ```bash
>     psql -U vendor_user -d vendor_db -f sql/ddl.sql
>     ```

### 🧹 2. Install Dependencies

> ```bash
> python -m venv .venv
> .venv\Scripts\activate # Windows
> pip install -r requirements.txt
> ```
> If you don’t have `requirements.txt`, install manually:
> ```bash
> pip install pandas sqlalchemy psycopg2-binary python-dateutil fuzzywuzzy python-Levenshtein
> ```

### 🔄 3. Run ETL (Clean + Load Data)

> **Place your raw CSV files into:** `data/raw/`
>
> **Then run the ETL script:**
> ```bash
> python etl/clean_load.py
> ```
> **This script will:**
> * Clean the raw CSVs
> * Standardize column names
> * Fix data types
> * Load everything into **PostgreSQL**

---

## 📊 Power BI Dashboard

> 1.  Open **Power BI Desktop**
> 2.  Connect to **PostgreSQL**
>     * Server: `localhost`
>     * Database: `vendor_db`
> 3.  **Load these tables:** `vendors`, `purchase\_orders`, `deliveries`, `invoices`, `po\_line\_items`
> 4.  **Create DAX measures** for KPIs
> 5.  Build dashboard visuals
> 6.  (Optional) Publish to Web for an interactive link

### Run Sample Analysis Queries:

> ```bash
> psql -U vendor_user -d vendor_db -f sql/sample_queries.sql
> ```

---

## 🛠️ Tech Stack

> * **Python** (ETL)
> * **PostgreSQL** (database)
> * **Power BI** (dashboard)
> * **SQLAlchemy / Pandas** (Python libraries)

---

## 📌 Project Summary

> This project demonstrates:
> * **Python ETL pipeline** creation
> * **SQL table design** & relational modeling
> * **Data cleaning & transformation** techniques
> * **Power BI dashboard** creation
> * **KPI-driven vendor analysis**

---

## 📬 Contact

**Mantaj Singh**
Data Analytics | Acadia University
**LinkedIn:** [https://www.linkedin.com/in/mantaj-s-9448a7271](https://www.linkedin.com/in/mantaj-s-9448a7271)
