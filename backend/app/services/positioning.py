from __future__ import annotations

import math
from statistics import median

from app.schemas import ClusterCenter, PositionedProduct, PositioningResponse, Product


QUADRANTS = {
    (False, False): "Short & Slim",
    (False, True): "Short & Wide",
    (True, False): "Long & Slim",
    (True, True): "Long & Wide",
}


def assign_quadrant(product: Product, length_split: float, width_split: float) -> str:
    is_long = product.length >= length_split
    is_wide = product.width >= width_split
    return QUADRANTS[(is_long, is_wide)]


def distance(product: Product, target: Product) -> float:
    return math.sqrt((product.length - target.length) ** 2 + (product.width - target.width) ** 2)


def build_positioning(products: list[Product], target_product_id: str = "A") -> PositioningResponse:
    length_split = round(median(product.length for product in products), 1)
    width_split = round(median(product.width for product in products), 1)
    cluster_ids, centers = kmeans(products, k=4)
    target = next((product for product in products if product.product_id == target_product_id), None)
    if target is None:
        target = products[0]
        target_product_id = target.product_id

    positioned: list[PositionedProduct] = []
    quadrant_counts = {name: 0 for name in QUADRANTS.values()}

    for product in products:
        quadrant = assign_quadrant(product, length_split, width_split)
        quadrant_counts[quadrant] += 1
        positioned.append(
            PositionedProduct(
                **product.model_dump(),
                quadrant=quadrant,
                cluster_id=cluster_ids[product.product_id],
                distance_from_target=round(distance(product, target), 2),
            )
        )

    return PositioningResponse(
        x_axis="length",
        y_axis="width",
        length_split=length_split,
        width_split=width_split,
        products=positioned,
        quadrant_counts=quadrant_counts,
        cluster_centers=centers,
        target_product_id=target_product_id,
    )


def find_similar_products(
    products: list[Product],
    target_product_id: str = "A",
    limit: int = 30,
) -> list[PositionedProduct]:
    positioning = build_positioning(products, target_product_id)
    target = next((product for product in positioning.products if product.product_id == target_product_id), None)
    if target is None:
        target = positioning.products[0]

    peers = [
        product
        for product in positioning.products
        if product.product_id != target_product_id and product.quadrant == target.quadrant
    ]

    return sorted(peers, key=lambda product: product.distance_from_target or 0)[:limit]


def kmeans(products: list[Product], k: int = 4, iterations: int = 18) -> tuple[dict[str, int], list[ClusterCenter]]:
    points = [(product.product_id, product.length, product.width) for product in products]
    sorted_points = sorted(points, key=lambda item: (item[1], item[2]))
    step = max(1, len(sorted_points) // k)
    centers = [(sorted_points[min(i * step, len(sorted_points) - 1)][1], sorted_points[min(i * step, len(sorted_points) - 1)][2]) for i in range(k)]

    assignments: dict[str, int] = {}
    for _ in range(iterations):
        buckets: dict[int, list[tuple[float, float]]] = {index: [] for index in range(k)}

        for product_id, length, width in points:
            cluster_id = min(
                range(k),
                key=lambda index: (length - centers[index][0]) ** 2 + (width - centers[index][1]) ** 2,
            )
            assignments[product_id] = cluster_id
            buckets[cluster_id].append((length, width))

        next_centers = []
        for index in range(k):
            bucket = buckets[index]
            if not bucket:
                next_centers.append(centers[index])
                continue
            next_centers.append(
                (
                    sum(point[0] for point in bucket) / len(bucket),
                    sum(point[1] for point in bucket) / len(bucket),
                )
            )

        if next_centers == centers:
            break
        centers = next_centers

    center_models = []
    for index, center in enumerate(centers):
        count = sum(1 for cluster_id in assignments.values() if cluster_id == index)
        center_models.append(
            ClusterCenter(
                cluster_id=index,
                length=round(center[0], 1),
                width=round(center[1], 1),
                count=count,
            )
        )

    return assignments, center_models
