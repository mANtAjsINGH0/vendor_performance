-- DDL: Core tables for Vendor Performance Analysis (PostgreSQL)

CREATE TABLE IF NOT EXISTS vendors (
  vendor_id SERIAL PRIMARY KEY,
  vendor_ext_id TEXT,
  vendor_name TEXT NOT NULL,
  country TEXT,
  category TEXT,
  rating NUMERIC
);

CREATE TABLE IF NOT EXISTS purchase_orders (
  po_id TEXT PRIMARY KEY,
  po_date DATE,
  vendor_id INTEGER REFERENCES vendors(vendor_id),
  department TEXT,
  total_amount NUMERIC,
  currency TEXT,
  status TEXT
);

CREATE TABLE IF NOT EXISTS po_line_items (
  line_id SERIAL PRIMARY KEY,
  po_id TEXT REFERENCES purchase_orders(po_id),
  sku TEXT,
  description TEXT,
  qty_ordered INTEGER,
  qty_received INTEGER,
 unit_price NUMERIC
);

CREATE TABLE IF NOT EXISTS invoices (
  invoice_id TEXT PRIMARY KEY,
  po_id TEXT REFERENCES purchase_orders(po_id),
  invoice_date DATE,
  invoice_amount NUMERIC,
  paid_date DATE,
  payment_terms INTEGER
);

CREATE TABLE IF NOT EXISTS deliveries (
  delivery_id SERIAL PRIMARY KEY,
  po_id TEXT REFERENCES purchase_orders(po_id),
  expected_date DATE,
  actual_date DATE,
  status TEXT,
  delay_days INTEGER
);
