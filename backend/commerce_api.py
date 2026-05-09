from __future__ import annotations

from base64 import b64encode
from typing import Any
from urllib.parse import urlencode
import json
import os
import time
from urllib.request import Request, urlopen

from services.product_offers import MockRetailerProvider, ProductOfferService, snapshot_to_dict

try:
    from fastapi import FastAPI
    from pydantic import BaseModel
except Exception:
    FastAPI = None
    BaseModel = object


class ProductQuery(BaseModel):
    name: str
    brand: str
    price: float
    sku: str | None = None
    category: str = "skincare"
    retailer_search_term: str | None = None
    retailer_search_terms: list[str] = []


class EbayBrowseRetailerProvider:
    def __init__(self, timeout_seconds: int = 6) -> None:
        self.client_id = os.getenv("EBAY_CLIENT_ID")
        self.client_secret = os.getenv("EBAY_CLIENT_SECRET")
        self.marketplace_id = os.getenv("EBAY_MARKETPLACE_ID", "EBAY_US")
        self.timeout_seconds = timeout_seconds
        self._access_token: str | None = None
        self._token_expires_at = 0.0

    def get_offers(self, product: dict[str, Any]) -> list[Any]:
        if not self.client_id or not self.client_secret:
            return []

        access_token = self._get_access_token()
        if not access_token:
            return []

        search_terms = [
            product.get("retailer_search_term"),
            *product.get("retailer_search_terms", []),
            f"{product.get('brand', '')} {product.get('name', '')}".strip(),
        ]
        search_term = next((term for term in search_terms if term), None)
        if not search_term:
            return []

        query = urlencode({"q": search_term, "limit": 4})
        request = Request(
            f"https://api.ebay.com/buy/browse/v1/item_summary/search?{query}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "X-EBAY-C-MARKETPLACE-ID": self.marketplace_id,
            },
        )

        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception:
            return []

        offers = []
        for item in payload.get("itemSummaries", []):
            price = item.get("price", {}).get("value")
            item_url = item.get("itemWebUrl")
            if price is None or not item_url:
                continue
            seller_name = item.get("seller", {}).get("username") or item.get("seller", {}).get("feedbackPercentage") or "eBay"
            shipping_options = item.get("shippingOptions", [])
            shipping_note = "Marketplace listing"
            if shipping_options:
                shipping_cost = shipping_options[0].get("shippingCost", {}).get("value")
                shipping_note = f"Shipping ${shipping_cost}" if shipping_cost is not None else "Shipping varies"

            offers.append(
                {
                    "retailer": str(seller_name),
                    "price": float(price),
                    "url": item_url,
                    "shipping_note": shipping_note,
                    "in_stock": item.get("availability") != "OUT_OF_STOCK",
                }
            )
        return offers

    def _get_access_token(self) -> str | None:
        if self._access_token and time.time() < self._token_expires_at:
            return self._access_token

        credentials = b64encode(f"{self.client_id}:{self.client_secret}".encode("utf-8")).decode("ascii")
        request = Request(
            "https://api.ebay.com/identity/v1/oauth2/token",
            data=urlencode(
                {
                    "grant_type": "client_credentials",
                    "scope": "https://api.ebay.com/oauth/api_scope",
                }
            ).encode("utf-8"),
            headers={
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                token_payload = json.loads(response.read().decode("utf-8"))
        except Exception:
            return None

        access_token = token_payload.get("access_token")
        expires_in = int(token_payload.get("expires_in", 7200))
        if not access_token:
            return None
        self._access_token = str(access_token)
        self._token_expires_at = time.time() + max(60, expires_in - 120)
        return self._access_token


def create_app() -> Any:
    if FastAPI is None:
        raise RuntimeError("Install fastapi and pydantic to run the commerce API scaffold.")

    app = FastAPI(title="BeautyBuzzi Commerce API", version="0.1.0")
    service = ProductOfferService(providers=[EbayBrowseRetailerProvider(), MockRetailerProvider()])

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/offers")
    def offers(query: ProductQuery) -> dict[str, Any]:
        snapshot = service.get_snapshot(_query_to_dict(query))
        return snapshot_to_dict(snapshot)

    return app


app = create_app() if FastAPI is not None else None


def _query_to_dict(query: ProductQuery) -> dict[str, Any]:
    if hasattr(query, "model_dump"):
        return query.model_dump()
    return query.dict()
