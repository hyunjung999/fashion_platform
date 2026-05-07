from collections import defaultdict
from typing import Dict, List

from app.schemas import Product, Review


def analyze_length(products: List[Product], reviews: List[Review]) -> Dict:
    brand_lengths = defaultdict(list)
    for product in products:
        if product.length is not None:
            brand_lengths[product.brand].append(product.length)

    brand_avg_lengths = {
        brand: sum(lengths) / len(lengths)
        for brand, lengths in brand_lengths.items()
        if lengths
    }

    length_keywords = ["길다", "짧다", "딱 맞다", "기장", "롱", "숏", "무릎", "발목", "발끝"]
    keyword_counts = defaultdict(int)
    height_preferences = defaultdict(lambda: {"long": 0, "short": 0, "normal": 0, "count": 0})

    for review in reviews:
        text = (review.review_text or "").lower()
        for kw in length_keywords:
            if kw in text:
                keyword_counts[kw] += 1

        height = review.height_cm
        if height is not None:
            if 150 <= height < 160:
                bucket = "150-159cm"
            elif 160 <= height < 170:
                bucket = "160-169cm"
            elif 170 <= height < 180:
                bucket = "170-179cm"
            elif 180 <= height <= 200:
                bucket = "180-200cm"
            else:
                bucket = None

            if bucket:
                height_preferences[bucket]["count"] += 1
                if any(word in text for word in ["길다", "롱"]):
                    height_preferences[bucket]["long"] += 1
                elif any(word in text for word in ["짧다", "숏"]):
                    height_preferences[bucket]["short"] += 1
                else:
                    height_preferences[bucket]["normal"] += 1

    return {
        "brand_avg_lengths": brand_avg_lengths,
        "length_keyword_counts": dict(keyword_counts),
        "height_preferences": dict(height_preferences),
        "recommendations": {
            "short_fit": "기장이 짧게 느껴질 수 있습니다.",
            "long_fit": "기장이 긴 편이라 편안합니다.",
            "standard_fit": "대체로 표준 기장으로 평가됩니다.",
        },
    }


def analyze_fit(products: List[Product], reviews: List[Review]) -> Dict:
    size_info = defaultdict(lambda: {"count": 0, "ratings": [], "avg_height": 0.0, "avg_weight": 0.0})
    size_label_counts = defaultdict(int)

    for review in reviews:
        size = (review.purchase_size or review.size_label or "unknown").strip() or "unknown"
        entry = size_info[size]
        entry["count"] += 1
        entry["ratings"].append(review.rating)
        if review.height_cm is not None:
            entry["avg_height"] += review.height_cm
        if review.weight_kg is not None:
            entry["avg_weight"] += review.weight_kg
        size_label_counts[size] += 1

    for size, entry in size_info.items():
        count = entry["count"]
        entry["avg_rating"] = sum(entry["ratings"]) / len(entry["ratings"]) if entry["ratings"] else 0.0
        entry["avg_height"] = entry["avg_height"] / count if count else 0.0
        entry["avg_weight"] = entry["avg_weight"] / count if count else 0.0
        del entry["ratings"]

    return {
        "size_info": dict(size_info),
        "size_label_counts": dict(size_label_counts),
    }


def analyze_color(products: List[Product], reviews: List[Review]) -> Dict:
    color_info = defaultdict(lambda: {"count": 0, "ratings": [], "positive": 0, "negative": 0})

    for review in reviews:
        color = (review.purchase_color or "unknown").strip() or "unknown"
        entry = color_info[color]
        entry["count"] += 1
        entry["ratings"].append(review.rating)
        if review.rating >= 4:
            entry["positive"] += 1
        else:
            entry["negative"] += 1

    for entry in color_info.values():
        entry["avg_rating"] = sum(entry["ratings"]) / len(entry["ratings"]) if entry["ratings"] else 0.0
        del entry["ratings"]

    return {
        "color_info": dict(color_info)
    }


def analyze_material(products: List[Product], reviews: List[Review]) -> Dict:
    material_info = defaultdict(lambda: {"count": 0, "ratings": []})

    for product in products:
        material = (product.material or "unknown").strip() or "unknown"
        entry = material_info[material]
        entry["count"] += 1
        entry["ratings"].append(product.rating)

    return {
        "material_info": {
            material: {
                "count": entry["count"],
                "avg_rating": sum(entry["ratings"]) / len(entry["ratings"]) if entry["ratings"] else 0.0,
            }
            for material, entry in material_info.items()
        }
    }