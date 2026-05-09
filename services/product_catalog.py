from __future__ import annotations

from typing import Any
import re


SEARCH_HINT_OVERRIDES: dict[tuple[str, str], str] = {
    ("Bulldog", "Daily Face Wash"): "Bulldog Skincare Original Face Wash",
    ("Kiehl's", "Invisible SPF 50 Moisturiser"): "Kiehl's Ultra Facial UV Defense SPF 50",
    ("The Ordinary", "Niacinamide 10% Serum"): "The Ordinary Niacinamide 10% + Zinc 1%",
    ("Paula's Choice", "BHA Exfoliant"): "Paula's Choice Skin Perfecting 2% BHA Liquid Exfoliant",
    ("CeraVe", "Hydrating Cream Cleanser"): "CeraVe Hydrating Facial Cleanser",
    ("Elta MD", "Hydrating SPF 50"): "EltaMD UV Daily Broad-Spectrum SPF 40",
    ("EltaMD", "Mineral SPF 50"): "EltaMD UV Physical Broad-Spectrum SPF 41",
    ("La Roche-Posay", "Hydrating Cream Cleanser"): "La Roche-Posay Toleriane Hydrating Gentle Cleanser",
    ("The Inkey List", "Hyaluronic Acid Serum"): "The INKEY List Hyaluronic Acid Serum",
    ("Supergoop", "Matte Finish Sunscreen"): "Supergoop Unseen Sunscreen SPF 40",
}


def _slugify(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").upper() or "ITEM"


def build_catalog_product(
    product: dict[str, Any],
    *,
    segment: str,
    collection: str,
    category: str,
) -> dict[str, Any]:
    normalized = dict(product)
    brand = str(normalized.get("brand", "BeautyBuzzi"))
    name = str(normalized.get("name", "Product"))
    normalized["sku"] = normalized.get("sku") or "-".join(
        [
            "BBZ",
            _slugify(segment),
            _slugify(collection),
            _slugify(brand),
            _slugify(name),
        ]
    )
    normalized["category"] = normalized.get("category", category)
    normalized["segment"] = normalized.get("segment", segment)
    normalized["collection"] = normalized.get("collection", collection)
    normalized["retailer_search_term"] = normalized.get("retailer_search_term") or SEARCH_HINT_OVERRIDES.get(
        (brand, name),
        f"{brand} {name}",
    )
    normalized["retailer_search_terms"] = normalized.get("retailer_search_terms") or [
        normalized["retailer_search_term"],
        f"{brand} {name}",
    ]
    return normalized


def enrich_product_list(
    products: list[dict[str, Any]],
    *,
    segment: str,
    collection: str,
    category: str,
) -> list[dict[str, Any]]:
    return [
        build_catalog_product(product, segment=segment, collection=collection, category=category)
        for product in products
    ]


def enrich_product_map(
    product_map: dict[str, list[dict[str, Any]]],
    *,
    segment: str,
    category: str,
) -> dict[str, list[dict[str, Any]]]:
    return {
        collection: enrich_product_list(
            products,
            segment=segment,
            collection=collection,
            category=category,
        )
        for collection, products in product_map.items()
    }
