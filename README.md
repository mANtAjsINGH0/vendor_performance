📊 Vendor Performance Analysis (Power BI + PostgreSQL + Python)

End-to-end project that cleans raw procurement data using Python, loads it into PostgreSQL, and builds an interactive Vendor Performance Dashboard in Power BI.

🚀 Features

Python ETL to clean, standardize, and load CSVs
PostgreSQL relational schema (vendors, purchase_orders, deliveries, invoices, po_line_items)

Power BI dashboard with KPIs:

Total Vendor Spend

Average Vendor Rating

Average Delivery Delay

Average Payment Days

Monthly Spend Trend

Vendor Comparison Charts

1. PostgreSQL Setup:
   
[Create DB + User]

CREATE ROLE vendor_user WITH LOGIN PASSWORD;

CREATE DATABASE vendor_db OWNER vendor_user;


[Run Table Schema]

psql -U vendor_user -d vendor_db -f sql/ddl.sql


🧹 2. Install Dependencies

python -m venv .venv

.\.venv\Scripts\activate    # Windows

pip install -r requirements.txt


If you don’t have requirements.txt, install manually:

pip install pandas sqlalchemy psycopg2-binary python-dateutil fuzzywuzzy python-Levenshtein


🔄 3. Run ETL (Clean + Load Data)

Place your CSV files into:
data/raw/

Then run:
python etl/clean_load.py

This will:
Clean the raw CSVs
Standardize column names
Fix data types
Load everything into PostgreSQL

4. Power BI Dashboard

~Open Power BI Desktop
~Connect to PostgreSQL
~Server: localhost
~Database: vendor_db

Load these tables:

~vendors

~purchase_orders

~deliveries

~invoices

~po_line_items

Create DAX measures for KPIs

Build dashboard visuals

(Optional) Publish to Web for an interactive link

Run Sample Analysis Queries:

psql -U vendor_user -d vendor_db -f sql/sample_queries.sql

🛠️ Tech Stack

Python (ETL)
PostgreSQL (database)
Power BI (dashboard)
SQLAlchemy / Pandas

📌 Project Summary

This project demonstrates:

Python ETL pipeline
SQL table design & relational modeling
Data cleaning & transformation
Power BI dashboard creation
KPI-driven vendor analysis

📬 Contact

Mantaj Singh
Data Analytics | Acadia University
LinkedIn: (https://www.linkedin.com/in/mantaj-s-9448a7271)

