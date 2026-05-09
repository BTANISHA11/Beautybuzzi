from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any
from urllib.parse import quote_plus
import json
import os
import time
from urllib.request import Request, urlopen

try:
    import streamlit as st
except Exception:
    st = None


@dataclass(frozen=True)
class RetailOffer:
    retailer: str
    price: float
    url: str
    shipping_note: str
    in_stock: bool = True


@dataclass(frozen=True)
class ProductOfferSnapshot:
    product_name: str
    brand: str
    best_offer: RetailOffer
    offers: list[RetailOffer]
    comparison_label: str
    source: str


class MockRetailerProvider:
    def get_offers(self, product: dict[str, Any]) -> list[RetailOffer]:
        base_price = float(product.get("price", 0))
        query = quote_plus(f"{product.get('brand', '')} {product.get('name', '')}".strip())
        retailers = [
            ("Amazon", 1.00, "https://www.amazon.com/s?k="),
            ("Walmart", 0.96, "https://www.walmart.com/search?q="),
            ("Target", 1.04, "https://www.target.com/s?searchTerm="),
        ]
        offers: list[RetailOffer] = []
        for retailer, multiplier, url_prefix in retailers:
            offers.append(
                RetailOffer(
                    retailer=retailer,
                    price=round(max(1.0, base_price * multiplier), 2),
                    url=f"{url_prefix}{query}",
                    shipping_note="Mock retailer data",
                )
            )
        return offers


class BackendApiRetailerProvider:
    def __init__(self, endpoint: str | None = None, timeout_seconds: float = 1.5) -> None:
        self.endpoint = endpoint or _get_config_value("BEAUTYBUZZI_COMMERCE_API")
        self.timeout_seconds = timeout_seconds
        self.last_source = "api"
        self._disabled_until = 0.0

    def get_offers(self, product: dict[str, Any]) -> list[RetailOffer]:
        if not self.endpoint:
            return []
        if time.time() < self._disabled_until:
            return []

        payload = json.dumps(
            {
                "name": product.get("name"),
                "brand": product.get("brand"),
                "price": product.get("price"),
                "sku": product.get("sku"),
                "category": product.get("category", "skincare"),
                "retailer_search_term": product.get("retailer_search_term"),
                "retailer_search_terms": product.get("retailer_search_terms", []),
            }
        ).encode("utf-8")
        request = Request(
            self.endpoint,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                response_data = json.loads(response.read().decode("utf-8"))
        except Exception:
            self._disabled_until = time.time() + 60
            return []

        self._disabled_until = 0.0
        self.last_source = str(response_data.get("source", "api"))

        offers: list[RetailOffer] = []
        for offer in response_data.get("offers", []):
            if not offer.get("retailer") or offer.get("price") is None or not offer.get("url"):
                continue
            offers.append(
                RetailOffer(
                    retailer=str(offer["retailer"]),
                    price=float(offer["price"]),
                    url=str(offer["url"]),
                    shipping_note=str(offer.get("shipping_note", "Live API result")),
                    in_stock=bool(offer.get("in_stock", True)),
                )
            )
        return offers


class ProductOfferService:
    def __init__(self, providers: list[Any] | None = None) -> None:
        self.providers = providers or [BackendApiRetailerProvider(), MockRetailerProvider()]

    def get_snapshot(self, product: dict[str, Any]) -> ProductOfferSnapshot:
        offers: list[RetailOffer] = []
        source = "mock"
        for provider in self.providers:
            offers = provider.get_offers(product)
            if offers:
                if isinstance(provider, BackendApiRetailerProvider) and provider.endpoint:
                    source = getattr(provider, "last_source", "api")
                else:
                    source = "mock"
                break

        if not offers:
            offers = MockRetailerProvider().get_offers(product)
            source = "mock"

        ordered_offers = sorted(offers, key=lambda offer: offer.price)
        best_offer = ordered_offers[0]
        price_span = ordered_offers[-1].price - best_offer.price if len(ordered_offers) > 1 else 0.0
        comparison_label = f"Save ${price_span:.2f} vs highest offer" if price_span > 0 else "Single retailer price"

        return ProductOfferSnapshot(
            product_name=str(product.get("name", "Product")),
            brand=str(product.get("brand", "Unknown brand")),
            best_offer=best_offer,
            offers=ordered_offers,
            comparison_label=comparison_label,
            source=source,
        )


def snapshot_to_dict(snapshot: ProductOfferSnapshot) -> dict[str, Any]:
    return {
        "product_name": snapshot.product_name,
        "brand": snapshot.brand,
        "comparison_label": snapshot.comparison_label,
        "source": snapshot.source,
        "best_offer": asdict(snapshot.best_offer),
        "offers": [asdict(offer) for offer in snapshot.offers],
    }


def _get_config_value(key: str) -> str | None:
    env_value = os.getenv(key)
    if env_value:
        return env_value
    if st is not None:
        try:
            secret_value = st.secrets.get(key)
        except Exception:
            secret_value = None
        if secret_value:
            return str(secret_value)
    return None
