# paystack.py
import requests
from django.conf import settings


PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY  # Replace with your real key
BASE_URL = 'https://api.paystack.co'


def initialize_transaction(email, amount, callback_url):
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "amount": int(amount) * 100,  # convert to kobo
        "callback_url": callback_url
    }
    response = requests.post(f"{BASE_URL}/transaction/initialize", json=data, headers=headers)
    return response.json()


def verify_transaction(reference):
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"
    }
    response = requests.get(f"{BASE_URL}/transaction/verify/{reference}", headers=headers)
    return response.json()
