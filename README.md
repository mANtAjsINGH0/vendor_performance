# Vendor Performance Analysis

This project turns raw procurement data (vendors, purchase orders, deliveries, invoices) into an analysis-ready PostgreSQL database and a vendor scorecard.

## Quick Start

1) **Get data**
   - Download a procurement dataset (e.g., Kaggle vendor/performance or public PO data) and place CSVs into `data/raw/`.

2) **Install PostgreSQL**
   - macOS:
     ```bash
     brew install postgresql
     brew services start postgresql
     ```
   - Windows: Install from postgresql.org with pgAdmin.

3) **Create database & user**
   ```bash
   psql -U postgres
   CREATE ROLE vendor_user WITH LOGIN PASSWORD 'vendor_pass';
   CREATE DATABASE vendor_db OWNER vendor_user;
   \q
   ```

4) **Create tables**
   ```bash
   psql -U vendor_user -d vendor_db -f sql/ddl.sql
   ```

5) **Clean + load the CSVs**
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install pandas sqlalchemy psycopg2-binary python-dateutil fuzzywuzzy python-Levenshtein
   python etl/clean_load.py
   ```

6) **Run sample queries**
   ```bash
   psql -U vendor_user -d vendor_db -f sql/sample_queries.sql
   ```
