import json
import csv
from pathlib import Path
from datetime import datetime

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Get latest order file
order_files = sorted(RAW_DIR.glob("paypal_order_*.json"), reverse=True)

if not order_files:
    raise RuntimeError("No PayPal order files found")

latest_file = order_files[0]
print(f"Using raw order file: {latest_file.name}")

with open(latest_file) as f:
    order = json.load(f)

purchase_units = order.get("purchase_units", [])
if not purchase_units:
    raise RuntimeError("No purchase units found")

payments = purchase_units[0].get("payments", {})
captures = payments.get("captures", [])

if not captures:
    raise RuntimeError("No captured payments found")

output_file = PROCESSED_DIR / f"payments_fact_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"

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

    for cap in captures:
        writer.writerow([
            cap.get("id"),
            cap.get("status"),
            cap.get("amount", {}).get("value"),
            cap.get("amount", {}).get("currency_code"),
            order.get("payer", {}).get("email_address"),
            "paypal",
            cap.get("create_time"),
            datetime.utcnow().isoformat()
        ])

print(f"✅ Payments fact CSV created → {output_file}")