from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app.data_sources.base import DataSource
from app.data_sources.csv_source import CSVDataSource
from app.schemas import MockDataResponse, PositionedProduct, PositioningResponse, ReviewAnalysisResponse
from app.services.analysis import analyze_color, analyze_fit, analyze_length, analyze_material
from app.services.positioning import build_positioning, find_similar_products
from app.services.review_analysis import build_review_analysis


app = FastAPI(
    title="여성 트레이닝 팬츠 시장 분석 API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

csv_source = CSVDataSource()


def get_data_source() -> DataSource:
    return csv_source


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


@app.get("/data", response_model=MockDataResponse)
def data_source(source: DataSource = Depends(get_data_source)) -> MockDataResponse:
    return mock_data(source)


@app.get("/positioning", response_model=PositioningResponse)
def positioning(
    product_id: str = Query(default="A"),
    source: DataSource = Depends(get_data_source),
) -> PositioningResponse:
    return build_positioning(source.get_products(), target_product_id=product_id)


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


@app.get("/length-analysis")
def length_analysis(source: DataSource = Depends(get_data_source)):
    return analyze_length(source.get_products(), source.get_reviews())


@app.get("/fit-analysis")
def fit_analysis(source: DataSource = Depends(get_data_source)):
    return analyze_fit(source.get_products(), source.get_reviews())


@app.get("/color-analysis")
def color_analysis(source: DataSource = Depends(get_data_source)):
    return analyze_color(source.get_products(), source.get_reviews())


@app.get("/material-analysis")
def material_analysis(source: DataSource = Depends(get_data_source)):
    return analyze_material(source.get_products(), source.get_reviews())
