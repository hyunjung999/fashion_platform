# 여성 트레이닝 팬츠 시장 분석 대시보드

Mock 데이터로 동작하는 풀스택 프로토타입입니다. 자사 상품 `Product A`의 포지셔닝, 동일 사분면 경쟁 상품 비교, 리뷰 기반 카테고리별 긍부정 인사이트를 제공합니다.

## 프로젝트 구조

```text
backend/
  app/
    data_sources/      # Mock/Real 데이터 소스 교체 지점
    services/          # 포지셔닝, 유사 상품, 리뷰 분석 로직
    main.py            # FastAPI 엔트리포인트
    schemas.py         # 데이터 스키마
  requirements.txt
frontend/
  src/
    components/
    pages/
    api.js
    App.jsx
    styles.css
  package.json
```

## 실행 방법

### 백엔드

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 프론트엔드

```bash
cd frontend
npm install
npm run dev
```

프론트엔드는 기본적으로 `http://localhost:8000` 백엔드 API를 호출합니다. 필요하면 `frontend/.env`에 `VITE_API_BASE_URL`을 설정하세요.

## 주요 API

- `GET /mock-data`
- `GET /positioning`
- `GET /similar-products?product_id=A`
- `GET /review-analysis?product_id=A`

## 실제 데이터 교체

`backend/app/data_sources/base.py`의 `DataSource` 인터페이스를 구현한 뒤 `backend/app/main.py`의 데이터 소스 생성 부분만 바꾸면 됩니다.
