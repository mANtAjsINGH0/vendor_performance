# ETL: Clean raw CSVs and load into PostgreSQL
import os
import pandas as pd
from dateutil import parser
from fuzzywuzzy import process
from sqlalchemy import create_engine

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW = os.path.join(BASE, "data", "raw")
CLEAN = os.path.join(BASE, "data", "cleaned")

COLUMN_MAPS = {
    "vendors": {
        "vendor_ext_id": ["vendor_id","id","supplier_id"],
        "vendor_name": ["vendor_name","name","supplier_name"],
        "country": ["country","country_name"],
        "category": ["category","segment","commodity"],
        "rating": ["rating","score","supplier_rating"]
    },
    "purchase_orders": {
        "po_id": ["po_id","po number","purchase_order_id","order_id"],
        "po_date": ["po_date","order_date","date"],
        "vendor_id": ["vendor_id","supplier_id"],
        "vendor_name": ["vendor_name","supplier_name","vendor"],
        "department": ["department","cost_center","dept"],
        "total_amount": ["total_amount","amount","po_value","total"],
        "currency": ["currency","ccy"],
        "status": ["status","po_status"]
    },
    "po_line_items": {
        "po_id": ["po_id","purchase_order_id","order_id"],
        "sku": ["sku","item_id","product_id","material_code"],
        "description": ["description","item_description","product_name"],
        "qty_ordered": ["qty_ordered","quantity","qty"],
        "qty_received": ["qty_received","received_qty","qty_rcvd"],
        "unit_price": ["unit_price","price","unit_cost"]
    },
    "invoices": {
        "invoice_id": ["invoice_id","inv_id","invoice number"],
        "po_id": ["po_id","purchase_order_id","order_id"],
        "invoice_date": ["invoice_date","date"],
        "invoice_amount": ["invoice_amount","amount","value"],
        "paid_date": ["paid_date","payment_date"],
        "payment_terms": ["payment_terms","terms_days"]
    },
    "deliveries": {
        "po_id": ["po_id","purchase_order_id","order_id"],
        "expected_date": ["expected_date","promise_date","eta"],
        "actual_date": ["actual_date","delivery_date","delivered_at"],
        "status": ["status","delivery_status"],
        "delay_days": ["delay_days","delay","days_delayed"]
    }
}

def rename_with_map(df, mapping):
    lower = {c.lower(): c for c in df.columns}
    out = {}
    for std, candidates in mapping.items():
        for cand in candidates:
            if cand.lower() in lower:
                out[std] = lower[cand.lower()]
                break
    return df.rename(columns=out)

def coerce_date(x):
    import pandas as pd
    if pd.isna(x) or x == "": return pd.NaT
    try: return parser.parse(str(x)).date()
    except Exception: return pd.NaT

def load_csv_guess(name):
    # If exact file exists, use it; else pick first file that contains the name
    exact = os.path.join(RAW, f"{name}.csv")
    if os.path.exists(exact):
        return pd.read_csv(exact)
    for f in os.listdir(RAW):
        if f.lower().endswith(".csv") and name in f.lower():
            return pd.read_csv(os.path.join(RAW, f))
    raise FileNotFoundError(f"Put a CSV for {name} under data/raw/")

def main():
    os.makedirs(CLEAN, exist_ok=True)
    vendors = rename_with_map(load_csv_guess("vendors"), COLUMN_MAPS["vendors"])
    po = rename_with_map(load_csv_guess("purchase_orders"), COLUMN_MAPS["purchase_orders"])
    # Map vendor_name to vendor_id
    vendor_map = vendors[['vendor_name']].copy()
    vendor_map['vendor_id'] = vendors.index + 1  # vendor_id from SERIAL sequence
    vendors['vendor_id'] = vendor_map['vendor_id']
    po = po.merge(vendor_map, on="vendor_name", how="left")
    po.drop(columns=["vendor_name"], inplace=True, errors="ignore")

    li = rename_with_map(load_csv_guess("po_line_items"), COLUMN_MAPS["po_line_items"])
    inv = rename_with_map(load_csv_guess("invoices"), COLUMN_MAPS["invoices"])
    try:
        deliv = rename_with_map(load_csv_guess("deliveries"), COLUMN_MAPS["deliveries"])
    except FileNotFoundError:
        deliv = pd.DataFrame(columns=["po_id","expected_date","actual_date","status","delay_days"])

    # types
    for c in ["rating"]: 
        if c in vendors: vendors[c] = pd.to_numeric(vendors[c], errors="coerce")

    # vendor name std
    vendors["vendor_name"] = vendors["vendor_name"].astype(str).str.strip().str.title()

    if "po_date" in po: po["po_date"] = po["po_date"].apply(coerce_date)
    if "total_amount" in po: po["total_amount"] = pd.to_numeric(po["total_amount"], errors="coerce")

    for c in ["qty_ordered","qty_received"]:
        if c in li: li[c] = pd.to_numeric(li[c], errors="coerce").fillna(0).astype("Int64")
    if "unit_price" in li: li["unit_price"] = pd.to_numeric(li["unit_price"], errors="coerce")

    for c in ["invoice_date","paid_date"]:
        if c in inv: inv[c] = inv[c].apply(coerce_date)
    if "invoice_amount" in inv: inv["invoice_amount"] = pd.to_numeric(inv["invoice_amount"], errors="coerce")

    for c in ["expected_date","actual_date"]:
        if c in deliv: deliv[c] = deliv[c].apply(coerce_date)
    if "delay_days" not in deliv and {"expected_date","actual_date"}.issubset(deliv.columns):
        deliv["delay_days"] = (pd.to_datetime(deliv["actual_date"]) - pd.to_datetime(deliv["expected_date"])).dt.days

    vendors.to_csv(os.path.join(CLEAN, "vendors.csv"), index=False)
    po.to_csv(os.path.join(CLEAN, "purchase_orders.csv"), index=False)
    li.to_csv(os.path.join(CLEAN, "po_line_items.csv"), index=False)
    inv.to_csv(os.path.join(CLEAN, "invoices.csv"), index=False)
    deliv.to_csv(os.path.join(CLEAN, "deliveries.csv"), index=False)

    # Load to Postgres
    user = os.getenv("PGUSER", "vendor_user")
    pw   = os.getenv("PGPASS", "vendor_pass")
    host = os.getenv("PGHOST", "localhost")
    db   = os.getenv("PGDB", "vendor_db")
    engine = create_engine(f"postgresql+psycopg2://{user}:{pw}@{host}/{db}")

    with engine.begin() as con:
        vendors.to_sql("vendors", con, schema="public", if_exists="append", index=False)
        po.to_sql("purchase_orders", con, schema="public", if_exists="append", index=False)
        li.to_sql("po_line_items", con, schema="public", if_exists="append", index=False)
        inv.to_sql("invoices", con, schema="public", if_exists="append", index=False)
        deliv.to_sql("deliveries", con, schema="public", if_exists="append", index=False)


    print("ETL complete.")

if __name__ == "__main__":
    main()
