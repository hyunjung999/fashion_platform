from __future__ import annotations

import random

from app.data_sources.base import DataSource
from app.schemas import Product, Review


BRANDS = [
    "Active Muse",
    "Move Lab",
    "DailyFit",
    "StudioRun",
    "Urban Flex",
    "Balance Wear",
    "Core Motion",
    "Fit&Form",
    "Ease Athletic",
    "North Yoga",
    "Mode Runner",
    "Haven Sports",
]

MATERIALS = [
    "폴리에스터 88%, 스판 12%",
    "나일론 82%, 스판 18%",
    "코튼 60%, 폴리에스터 35%, 스판 5%",
    "모달 45%, 폴리에스터 50%, 스판 5%",
    "리사이클 폴리 80%, 스판 20%",
]

POSITIVE_PHRASES = {
    "품질": ["봉제가 탄탄하고 여러 번 세탁해도 형태가 잘 유지돼요", "마감이 깔끔해서 오래 입을 수 있을 것 같아요"],
    "사이즈": ["정사이즈로 고르면 허리와 기장이 잘 맞아요", "사이즈 안내가 정확해서 교환 없이 입었어요"],
    "가격": ["가격 대비 완성도가 좋아서 만족스러워요", "행사 가격으로 사니 가성비가 확실히 좋네요"],
    "컬러": ["컬러가 화면과 거의 같고 차분해서 코디하기 쉬워요", "색감이 세련돼서 운동복 느낌이 과하지 않아요"],
    "소재": ["소재가 부드럽고 신축성이 좋아 움직임이 편해요", "땀이 나도 금방 마르는 느낌이라 운동할 때 좋아요"],
    "구매여정": ["배송이 빠르고 포장이 깔끔하게 도착했어요", "상세 설명이 충분해서 구매 결정이 쉬웠어요"],
    "핏": ["허벅지 라인을 자연스럽게 잡아줘서 핏이 예뻐요", "일자로 떨어지는 실루엣이 다리를 길어 보이게 해요"],
    "디테일": ["허리 밴딩과 포켓 디테일이 실용적이에요", "스트링 마감이 단정해서 전체적으로 완성도가 높아요"],
}

NEGATIVE_PHRASES = {
    "품질": ["몇 번 입지 않았는데 보풀이 조금 올라왔어요", "봉제선이 한쪽만 살짝 울어서 아쉬워요"],
    "사이즈": ["허리가 생각보다 작게 나와서 한 치수 크게 살 걸 그랬어요", "기장이 애매해서 키가 작은 사람에게는 길 수 있어요"],
    "가격": ["정가로 사기에는 가격이 조금 부담스러워요", "비슷한 제품과 비교하면 할인 없이는 비싸게 느껴져요"],
    "컬러": ["실제 색상이 화면보다 조금 어둡게 느껴졌어요", "밝은 컬러는 속옷 라인이 살짝 비쳐요"],
    "소재": ["원단이 기대보다 얇아서 겨울에는 추울 것 같아요", "피부에 닿는 느낌이 약간 까슬하게 느껴졌어요"],
    "구매여정": ["배송이 예정보다 늦어서 바로 입지 못했어요", "상세 페이지 치수 정보가 더 자세했으면 좋겠어요"],
    "핏": ["골반 부분이 살짝 뜨고 무릎 아래가 어색하게 떨어져요", "통이 생각보다 넓어서 슬림한 느낌은 아니에요"],
    "디테일": ["주머니가 얕아서 휴대폰을 넣기 불안해요", "허리 스트링 끝 마감이 조금 약해 보여요"],
}

NEUTRAL_PHRASES = [
    "평소 운동과 가벼운 외출용으로 입기 무난합니다",
    "전체적으로 설명과 비슷한 상품이에요",
    "특별히 튀지 않고 기본 아이템으로 괜찮습니다",
]


class MockDataSource(DataSource):
    def __init__(self, seed: int = 430) -> None:
        self._random = random.Random(seed)
        self._products = self._build_products()
        self._reviews = self._build_reviews()

    def get_products(self) -> list[Product]:
        return self._products

    def get_reviews(self) -> list[Review]:
        return self._reviews

    def _build_products(self) -> list[Product]:
        products = [
            Product(
                product_id="A",
                brand="자사 Product A",
                price=59000,
                length=99.5,
                width=30.8,
                material="나일론 82%, 스판 18%",
                rating=4.6,
            )
        ]

        for index in range(1, 121):
            brand = self._random.choice(BRANDS)
            base_length = self._random.choice([88, 92, 96, 100, 104])
            base_width = self._random.choice([26, 28, 30, 32, 35])
            price = int(self._random.randrange(29000, 129000, 1000))
            products.append(
                Product(
                    product_id=f"P{index:03d}",
                    brand=brand,
                    price=price,
                    length=round(base_length + self._random.uniform(-3.2, 3.8), 1),
                    width=round(base_width + self._random.uniform(-1.8, 2.2), 1),
                    material=self._random.choice(MATERIALS),
                    rating=round(self._random.uniform(3.4, 4.9), 1),
                )
            )

        return products

    def _build_reviews(self) -> list[Review]:
        reviews: list[Review] = []

        for product in self._products:
            count = self._random.randint(8, 20) if product.product_id == "A" else self._random.randint(5, 18)
            for _ in range(count):
                category = self._random.choice(list(POSITIVE_PHRASES.keys()))
                sentiment_roll = self._random.random()

                if product.product_id == "A":
                    sentiment_roll += 0.12

                if sentiment_roll > 0.68:
                    text = self._random.choice(POSITIVE_PHRASES[category])
                    rating = self._random.choice([4, 5, 5])
                elif sentiment_roll < 0.28:
                    text = self._random.choice(NEGATIVE_PHRASES[category])
                    rating = self._random.choice([2, 3, 3])
                else:
                    text = self._random.choice(NEUTRAL_PHRASES)
                    rating = self._random.choice([3, 4])

                reviews.append(
                    Review(
                        product_id=product.product_id,
                        review_text=text,
                        rating=rating,
                    )
                )

        return reviews
