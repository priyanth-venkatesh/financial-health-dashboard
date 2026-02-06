import requests


def fetch_bank_transactions(api_url: str, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(api_url, headers=headers).json()


def fetch_gst_data(gst_api: str, gstin: str):
    return requests.get(f"{gst_api}/{gstin}").json()