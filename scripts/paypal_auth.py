import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
SECRET = os.getenv("PAYPAL_SECRET")

url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"

auth = base64.b64encode(f"{CLIENT_ID}:{SECRET}".encode()).decode()

headers = {
    "Authorization": f"Basic {auth}",
    "Content-Type": "application/x-www-form-urlencoded"
}

data = {"grant_type": "client_credentials"}

response = requests.post(url, headers=headers, data=data)
response.raise_for_status()

access_token = response.json()["access_token"]
print(access_token)