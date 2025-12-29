import requests
from django.conf import settings


class BOSClient:
    def __init__(self, client):
        self.client = client
        self.base_url = settings.BOS_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {settings.BOS_SERVICE_TOKEN}",
            "Content-Type": "application/json",
        }

    def get_bills(self, start_date, end_date):
        resp = requests.get(
            f"{self.base_url}/api/sales/bills/",
            headers=self.headers,
            params={
                "date__gte": start_date,
                "date__lte": end_date,
            },
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
