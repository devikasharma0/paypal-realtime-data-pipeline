import json
import csv
import os
from datetime import datetime

RAW_DIR = "data/raw"
OUTPUT_DIR = "data/processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get latest raw file
raw_files = sorted(
    [f for f in os.listdir(RAW_DIR) if f.startswith("paypal_payments")],
    reverse=True
)

if not raw_files:
    raise Exception("No raw PayPal payment files found")

latest_file = os.path.join(RAW_DIR, raw_files[0])

with open(latest_file, "r") as f:
    data = json.load(f)

payments = data.get("payments", [])

output_file = os.path.join(
    OUTPUT_DIR,
    f"payments_fact_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
)

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

    for p in payments:
        txn = p.get("transactions", [{}])[0]
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

print(f"Processed {len(payments)} payments → {output_file}")