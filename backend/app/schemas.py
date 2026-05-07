from pydantic import BaseModel, Field


class Product(BaseModel):
    product_id: str
    name: str | None = None
    brand: str
    price: int
    length: float = Field(description="총장(cm)")
    width: float = Field(description="통/허벅지/힙 기준 너비(cm)")
    material: str
    rating: float


class Review(BaseModel):
    review_id: str | None = None
    product_id: str
    product_name: str | None = None
    review_text: str
    rating: int
    created_at: str | None = None
    purchase_color: str | None = None
    purchase_size: str | None = None
    size_label: str | None = None
    quality_assessment: str | None = None
    color_assessment: str | None = None
    height_cm: float | None = None
    weight_kg: float | None = None
    usual_size: str | None = None


class PositionedProduct(Product):
    quadrant: str
    cluster_id: int
    distance_from_target: float | None = None


class ClusterCenter(BaseModel):
    cluster_id: int
    length: float
    width: float
    count: int


class PositioningResponse(BaseModel):
    x_axis: str
    y_axis: str
    length_split: float
    width_split: float
    products: list[PositionedProduct]
    quadrant_counts: dict[str, int]
    cluster_centers: list[ClusterCenter]
    target_product_id: str = "A"


class MockDataResponse(BaseModel):
    products: list[Product]
    reviews: list[Review]
    product_count: int
    review_count: int


class CategoryInsight(BaseModel):
    category: str
    positive_summary: str
    negative_summary: str
    keywords: list[str]
    positive_count: int
    negative_count: int
    neutral_count: int


class ReviewAnalysisGroup(BaseModel):
    label: str
    product_ids: list[str]
    total_reviews: int
    categories: list[CategoryInsight]


class ReviewAnalysisResponse(BaseModel):
    target: ReviewAnalysisGroup
    competitors: ReviewAnalysisGroup
