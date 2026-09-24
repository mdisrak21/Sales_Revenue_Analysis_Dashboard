from pathlib import Path
import io
import zipfile
import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

# Official UCI download endpoint linked from the dataset's Files page.
UCI_ZIP = "https://cdn.uci-ics-mlr-prod.aws.uci.edu/352/online%2Bretail.zip"

def download_dataset():
    target = RAW / "Online Retail.xlsx"
    if target.exists():
        print(f"Already exists: {target}")
        return target

    print("Downloading UCI Online Retail dataset...")
    r = requests.get(UCI_ZIP, timeout=120)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        names = z.namelist()
        xlsx = next((n for n in names if n.lower().endswith(".xlsx")), None)
        if not xlsx:
            raise FileNotFoundError("No .xlsx file found in the UCI archive.")
        with z.open(xlsx) as src, open(target, "wb") as dst:
            dst.write(src.read())

    print(f"Saved: {target}")
    return target

if __name__ == "__main__":
    download_dataset()
