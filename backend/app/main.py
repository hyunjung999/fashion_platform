from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app.data_sources.base import DataSource
from app.data_sources.mock_source import MockDataSource
from app.schemas import MockDataResponse, PositionedProduct, PositioningResponse, ReviewAnalysisResponse
from app.services.positioning import build_positioning, find_similar_products
from app.services.review_analysis import build_review_analysis


app = FastAPI(
    title="여성 트레이닝 팬츠 시장 분석 API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mock_source = MockDataSource()


def get_data_source() -> DataSource:
    return mock_source


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/mock-data", response_model=MockDataResponse)
def mock_data(source: DataSource = Depends(get_data_source)) -> MockDataResponse:
    products = source.get_products()
    reviews = source.get_reviews()
    return MockDataResponse(
        products=products,
        reviews=reviews,
        product_count=len(products),
        review_count=len(reviews),
    )


@app.get("/positioning", response_model=PositioningResponse)
def positioning(source: DataSource = Depends(get_data_source)) -> PositioningResponse:
    return build_positioning(source.get_products())


@app.get("/similar-products", response_model=list[PositionedProduct])
def similar_products(
    product_id: str = Query(default="A"),
    limit: int = Query(default=30, ge=1, le=100),
    source: DataSource = Depends(get_data_source),
) -> list[PositionedProduct]:
    return find_similar_products(source.get_products(), target_product_id=product_id, limit=limit)


@app.get("/review-analysis", response_model=ReviewAnalysisResponse)
def review_analysis(
    product_id: str = Query(default="A"),
    source: DataSource = Depends(get_data_source),
) -> ReviewAnalysisResponse:
    target, competitors = build_review_analysis(
        source.get_products(),
        source.get_reviews(),
        target_product_id=product_id,
    )
    return ReviewAnalysisResponse(target=target, competitors=competitors)
