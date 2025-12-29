import requests
from django.conf import settings
from .auth import BOSAuth

class BOSClient:
    def __init__(self, base_url, auth: BOSAuth):
        self.base_url = base_url.rstrip("/")
        self.auth = auth

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.auth.get_access_token()}",
            "Content-Type": "application/json",
        }

    def _get(self, path, params=None):
        url = f"{self.base_url}{path}"
        resp = requests.get(
            url,
            headers=self._headers(),
            params=params,
            timeout=10,
        )

        # 🔁 Token expired → refresh once
        if resp.status_code == 401:
            self.auth.refresh()
            resp = requests.get(
                url,
                headers=self._headers(),
                params=params,
                timeout=10,
            )

        resp.raise_for_status()
        return resp.json()

    def get_customer_by_phone(self, phone: str):
        data = self._get(
            "/api/sales/customers/",
            params={"search": phone},
        )
        if not data:
            return None
        return data[0]  # first match

    def get_bills(self, customer_id: int, limit=20):
        bills = self._get(
            "/api/sales/bills/",
            params={"customer": customer_id},
        )
        return bills[:limit]


    def get_payments(self, customer_id: int):
        return self._get(
            "/api/sales/payments/",
            params={"customer": customer_id},
        )


# ---------- INVENTORY ----------

    def get_categories(self):
        return self._get("/api/inventory/categories/", params={"status": "active"})

    def get_products(self, category_id=None, search=None):
        params = {"status": "active"}

        if category_id:
            params["category"] = category_id

        if search:
            params["search"] = search

        print("DEBUG BOS: GET /products params =", params)

        data = self._get("/api/inventory/products/", params=params)

        print("DEBUG BOS: response =", data)
        return data

    def get_product_images(self, product_id):
        return self._get(f"/api/inventory/products/{product_id}/images/")

    def get_bills_by_date_range(self, start_date, end_date):
        return self._get(
            "/api/sales/bills/",
            params={
                "date__gte": start_date,
                "date__lte": end_date,
            },
        )