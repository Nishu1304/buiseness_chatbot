import requests
from django.conf import settings


class BOSAuth:
    def __init__(self):
        self.base_url = settings.BOS_BASE_URL.rstrip("/")
        self.email = settings.BOS_EMAIL
        self.password = settings.BOS_PASSWORD

        self.access_token = None
        self.refresh_token = None

    def login(self):
        url = f"{self.base_url}/api/token/"
        resp = requests.post(
            url,
            json={
                "email": self.email,
                "password": self.password,
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        self.access_token = data["access"]
        self.refresh_token = data["refresh"]

    def refresh(self):
        url = f"{self.base_url}/api/token/refresh/"
        resp = requests.post(
            url,
            json={"refresh": self.refresh_token},
            timeout=10,
        )
        resp.raise_for_status()
        self.access_token = resp.json()["access"]

    def get_access_token(self):
        if not self.access_token:
            self.login()
        return self.access_token
