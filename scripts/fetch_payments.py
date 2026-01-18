import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import subprocess

print("Starting PayPal fetch script...")

load_dotenv()

print("Fetching access token...")
access_token = subprocess.check_output(
    ["python3", "scripts/paypal_auth.py"]
).decode().strip()
print("Access token received.")

url = "https://api-m.sandbox.paypal.com/v1/payments/payment"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

params = {
    "count": 10
}

response = requests.get(url, headers=headers, params=params)
print("API response status:", response.status_code)

response.raise_for_status()
data = response.json()

os.makedirs("data/raw", exist_ok=True)

file_path = f"data/raw/paypal_payments_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"

with open(file_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved raw payments data to {file_path}")