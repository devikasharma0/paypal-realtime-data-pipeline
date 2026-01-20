import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import subprocess

print("Starting PayPal ORDERS fetch...")

load_dotenv()

# Get access token
access_token = subprocess.check_output(
    ["python3", "scripts/paypal_auth.py"]
).decode().strip()

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Replace with your actual approved Order ID
ORDER_ID = input("Enter approved Order ID: ").strip()

url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{ORDER_ID}"

response = requests.get(url, headers=headers)
response.raise_for_status()

order = response.json()

os.makedirs("data/raw", exist_ok=True)

file_path = f"data/raw/paypal_order_{ORDER_ID}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"

with open(file_path, "w") as f:
    json.dump(order, f, indent=2)

print(f"Saved raw order data to {file_path}")