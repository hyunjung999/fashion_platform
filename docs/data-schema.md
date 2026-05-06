# 데이터 스키마 설계

## Product

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `product_id` | string | 상품 식별자. 자사 상품은 `A` |
| `brand` | string | 브랜드명 |
| `price` | integer | 판매가 |
| `length` | number | 총장(cm), 포지셔닝 X축 |
| `width` | number | 통/허벅지/힙 기준 너비(cm), 포지셔닝 Y축 |
| `material` | string | 소재 구성 |
| `rating` | number | 상품 평균 평점 |

## Review

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `product_id` | string | 리뷰가 연결된 상품 ID |
| `review_text` | string | 자연어 리뷰 본문 |
| `rating` | integer | 리뷰 평점 |

## 분석 파생 필드

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `quadrant` | string | 중앙값 기준 4사분면: `Short & Slim`, `Short & Wide`, `Long & Slim`, `Long & Wide` |
| `cluster_id` | integer | 총장/통 기반 K-means 클러스터 ID |
| `distance_from_target` | number | Product A와의 유클리드 거리 |

## 실제 데이터 교체 원칙

백엔드는 `DataSource` 인터페이스를 통해 데이터 입출력을 분리합니다. 현재는 `MockDataSource`가 메모리에서 데이터를 생성하지만, CSV/DB/API 연동 시 `DataSource`를 구현한 새 클래스를 만들고 `main.py`의 의존성만 교체하면 됩니다.
