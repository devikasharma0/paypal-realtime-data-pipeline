import requests
import subprocess

access_token = subprocess.check_output(
    ["python3", "scripts/paypal_auth.py"]
).decode().strip()

url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

payload = {
    "intent": "CAPTURE",
    "purchase_units": [
        {
            "reference_id": "TEST_PAYMENT",
            "amount": {
                "currency_code": "USD",
                "value": "10.00"
            }
        }
    ],
    "payment_source": {
        "paypal": {
            "experience_context": {
                "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                "user_action": "PAY_NOW"
            }
        }
    }
}

response = requests.post(url, headers=headers, json=payload)
response.raise_for_status()

order = response.json()
print("Order ID:", order["id"])