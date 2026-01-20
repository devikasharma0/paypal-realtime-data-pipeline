import requests
import subprocess

# Get access token
access_token = subprocess.check_output(
    ["python3", "scripts/paypal_auth.py"]
).decode().strip()

ORDER_ID = input("Enter approved Order ID: ").strip()

url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{ORDER_ID}/capture"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers)
print("Status:", response.status_code)
print(response.text)

response.raise_for_status()

print("✅ Order captured successfully")