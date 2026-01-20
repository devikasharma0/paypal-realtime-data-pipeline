import json
import csv
from pathlib import Path
from datetime import datetime

RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Get latest raw PayPal payments file
raw_files = sorted(
    RAW_DIR.glob("paypal_payments_*.json"),
    reverse=True
)

if not raw_files:
    raise RuntimeError("No raw PayPal payment files found")

latest_file = raw_files[0]
print(f"Using raw file: {latest_file.name}")

with open(latest_file) as f:
    data = json.load(f)

# PayPal sandbox returns 'payments' array OR 'transactions'
payments = data.get("payments") or data.get("transactions") or []

if not payments:
    raise RuntimeError("No payment records found in raw data")

output_file = OUTPUT_DIR / f"payments_fact_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"

with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "payment_id",
        "status",
        "amount",
        "currency",
        "payer_email",
        "payment_method",
        "create_time",
        "ingestion_time"
    ])

    rows_written = 0

    for p in payments:
        txn = (p.get("transactions") or [{}])[0]
        amount_info = txn.get("amount", {})

        writer.writerow([
            p.get("id"),
            p.get("state"),
            amount_info.get("total"),
            amount_info.get("currency"),
            p.get("payer", {}).get("payer_info", {}).get("email"),
            p.get("payer", {}).get("payment_method"),
            p.get("create_time"),
            datetime.utcnow().isoformat()
        ])

        rows_written += 1

print(f"✅ Wrote {rows_written} payment rows → {output_file}")