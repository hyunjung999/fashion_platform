from pathlib import Path
from typing import Any

import pandas as pd

from app.data_sources.base import DataSource
from app.schemas import Product, Review


class CSVDataSource(DataSource):
    def __init__(self, data_dir: str | Path | None = None):
        if data_dir is None:
            self.data_dir = Path(__file__).resolve().parents[2] / "data"
        else:
            self.data_dir = Path(data_dir)
        self._raw_rows: list[dict[str, Any]] = []
        self._products: list[Product] = []
        self._reviews: list[Review] = []
        self._load_data()

    def get_products(self) -> list[Product]:
        return self._products

    def get_reviews(self) -> list[Review]:
        return self._reviews

    def _load_data(self) -> None:
        self._raw_rows = self._collect_review_rows()
        self._reviews = self._build_reviews(self._raw_rows)
        self._products = self._build_products(self._raw_rows)

    def _collect_review_rows(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for source_file in sorted(self.data_dir.glob("*")):
            if source_file.suffix.lower() not in {".csv", ".xls", ".xlsx"}:
                continue
            try:
                df = self._read_dataframe(source_file)
                df = self._normalize_columns(df)
                if "product_id" not in df.columns or "review_text" not in df.columns:
                    continue
                for _, row in df.iterrows():
                    rows.append(row.to_dict())
            except Exception as exc:
                print(f"Error loading {source_file}: {exc}")
        return rows

    def _build_reviews(self, rows: list[dict[str, Any]]) -> list[Review]:
        reviews: list[Review] = []
        for row in rows:
            product_id = self._to_str(row.get("product_id"))
            if not product_id:
                continue

            reviews.append(
                Review(
                    review_id=self._to_str(row.get("review_id")),
                    product_id=product_id,
                    product_name=self._to_str(row.get("product_name")),
                    review_text=self._to_str(row.get("review_text")) or "",
                    rating=self._to_int(row.get("rating")) or 0,
                    created_at=self._to_str(row.get("created_at")),
                    purchase_color=self._to_str(row.get("purchase_color")),
                    purchase_size=self._to_str(row.get("purchase_size")),
                    size_label=self._to_str(row.get("size_label")),
                    quality_assessment=self._to_str(row.get("quality_assessment")),
                    color_assessment=self._to_str(row.get("color_assessment")),
                    height_cm=self._to_float(row.get("height_cm")),
                    weight_kg=self._to_float(row.get("weight_kg")),
                    usual_size=self._to_str(row.get("usual_size")),
                )
            )
        return reviews

    def _build_products(self, rows: list[dict[str, Any]]) -> list[Product]:
        groups: dict[str, dict[str, Any]] = {}
        for row in rows:
            pid = self._to_str(row.get("product_id"))
            if not pid:
                continue
            if pid not in groups:
                name = self._to_str(row.get("product_name"))
                groups[pid] = {
                    "name": name,
                    "brand": self._extract_brand(name),
                    "ratings": [],
                    "length": self._extract_length(name),
                    "width": self._extract_width(name),
                    "material": self._extract_material(name),
                    "price": self._extract_price(name),
                }
            rating = self._to_int(row.get("rating"))
            if rating is not None:
                groups[pid]["ratings"].append(rating)

        products: list[Product] = []
        for pid, data in groups.items():
            avg_rating = sum(data["ratings"]) / len(data["ratings"]) if data["ratings"] else 4.0
            products.append(
                Product(
                    product_id=pid,
                    name=data["name"],
                    brand=data["brand"],
                    price=data["price"],
                    length=data["length"],
                    width=data["width"],
                    material=data["material"],
                    rating=round(avg_rating, 1),
                )
            )
        return products

    def _normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        rename_map = {
            "review_id": "review_id",
            "product_id": "product_id",
            "product_name": "product_name",
            "rating": "rating",
            "contents": "review_text",
            "review_text": "review_text",
            "created_at": "created_at",
            "like_count": "like_count",
            "구매컬러": "purchase_color",
            "구매사이즈": "purchase_size",
            "사이즈": "size_label",
            "퀄리티": "quality_assessment",
            "색감": "color_assessment",
            "키": "height_cm",
            "몸무게": "weight_kg",
            "평소사이즈": "usual_size",
        }
        normalized = {}
        for col in df.columns:
            key = str(col).strip()
            normalized[key] = rename_map.get(key, rename_map.get(key.lower(), key))
        return df.rename(columns=normalized)

    def _read_dataframe(self, source_file: Path) -> pd.DataFrame:
        suffix = source_file.suffix.lower()
        if suffix == ".csv":
            encodings = ["utf-8", "cp949", "euc-kr", "latin1"]
            last_exception = None
            for encoding in encodings:
                try:
                    return pd.read_csv(
                        source_file,
                        encoding=encoding,
                        on_bad_lines="skip",
                        engine="python",
                    )
                except Exception as exc:
                    last_exception = exc
                    continue
            raise last_exception
        if suffix in {".xls", ".xlsx"}:
            return pd.read_excel(source_file)
        raise ValueError(f"Unsupported file type: {source_file}")

    def _extract_brand(self, product_name: str | None) -> str:
        if not product_name:
            return "기타"
        if "베이델리" in product_name:
            return "베이델리"
        if "블랙업" in product_name:
            return "블랙업"
        if "슬로우앤드" in product_name:
            return "슬로우앤드"
        if "핫핑" in product_name:
            return "핫핑"
        if "크러시제이" in product_name:
            return "크러시제이"
        if "유리에" in product_name:
            return "유리에"
        if "데일리브" in product_name:
            return "데일리브"
        if "라룸" in product_name:
            return "라룸"
        if "미쏘" in product_name:
            return "미쏘"
        if "무신사" in product_name:
            return "무신사"
        if "mixxo" in product_name.lower():
            return "mixxo"
        return "기타"

    def _extract_length(self, product_name: str | None) -> float:
        if not product_name:
            return 100.0
        lower = product_name.lower()
        if "롱" in lower:
            return 105.0
        if "숏" in lower:
            return 95.0
        return 100.0

    def _extract_width(self, product_name: str | None) -> float:
        if not product_name:
            return 30.0
        if "와이드" in product_name:
            return 35.0
        if "부츠컷" in product_name:
            return 32.0
        if "조거" in product_name:
            return 31.0
        return 30.0

    def _extract_material(self, product_name: str | None) -> str:
        if not product_name:
            return "폴리에스터 혼방"
        if "코튼" in product_name:
            return "코튼 혼방"
        if "스웨트" in product_name or "스웻" in product_name:
            return "스웨트"
        if "니트" in product_name:
            return "니트"
        if "본딩" in product_name:
            return "본딩"
        return "폴리에스터 혼방"

    def _extract_price(self, product_name: str | None) -> int:
        return 50000

    def _to_str(self, value: Any) -> str | None:
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return None
        return str(value).strip()

    def _to_int(self, value: Any) -> int | None:
        try:
            return int(float(value))
        except Exception:
            return None

    def _to_float(self, value: Any) -> float | None:
        try:
            return float(value)
        except Exception:
            return None
