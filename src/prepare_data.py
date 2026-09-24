from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

def load_source(path=None):
    path = Path(path) if path else RAW / "Online Retail.xlsx"
    if path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    return pd.read_csv(path, encoding_errors="ignore")

def clean_sales_data(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    required = ["InvoiceNo","StockCode","Description","Quantity","InvoiceDate","UnitPrice","CustomerID","Country"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["InvoiceNo"] = df["InvoiceNo"].astype(str).str.strip()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df["Description"] = df["Description"].fillna("Unknown Product").astype(str).str.strip()
    df["Country"] = df["Country"].fillna("Unknown").astype(str).str.strip()

    df["IsCancellation"] = df["InvoiceNo"].str.upper().str.startswith("C")

    # Sales view: valid positive sales only, excluding cancelled invoices.
    sales = df.loc[
        (~df["IsCancellation"]) &
        (df["InvoiceDate"].notna()) &
        (df["Quantity"] > 0) &
        (df["UnitPrice"] > 0)
    ].copy()

    sales["Revenue"] = sales["Quantity"] * sales["UnitPrice"]
    sales["OrderDate"] = sales["InvoiceDate"].dt.date
    sales["Year"] = sales["InvoiceDate"].dt.year
    sales["Month"] = sales["InvoiceDate"].dt.to_period("M").astype(str)
    sales["MonthName"] = sales["InvoiceDate"].dt.strftime("%b")
    sales["YearMonth"] = sales["InvoiceDate"].dt.to_period("M").dt.to_timestamp()
    sales["CustomerID"] = sales["CustomerID"].astype("Int64")

    return sales

if __name__ == "__main__":
    source = RAW / "Online Retail.xlsx"
    sales = clean_sales_data(load_source(source))
    output = OUT / "online_retail_clean.csv"
    sales.to_csv(output, index=False)
    print(f"Saved {len(sales):,} cleaned rows to {output}")
