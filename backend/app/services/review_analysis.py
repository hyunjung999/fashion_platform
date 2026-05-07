from __future__ import annotations

from collections import Counter, defaultdict

from app.schemas import CategoryInsight, Product, Review, ReviewAnalysisGroup
from app.services.positioning import build_positioning


CATEGORY_KEYWORDS = {
    "품질": ["품질", "봉제", "마감", "세탁", "형태", "보풀", "튼튼", "완성도"],
    "사이즈": ["사이즈", "정사이즈", "허리", "치수", "기장", "한 치수"],
    "가격": ["가격", "가성비", "정가", "할인", "비싸", "부담"],
    "컬러": ["컬러", "색", "색감", "화면", "어둡", "비쳐"],
    "소재": ["소재", "원단", "신축성", "부드럽", "얇", "까슬", "땀"],
    "구매여정": ["배송", "포장", "상세", "구매", "교환", "도착"],
    "핏": ["핏", "실루엣", "라인", "골반", "무릎", "슬림", "일자"],
    "디테일": ["디테일", "포켓", "주머니", "스트링", "밴딩", "마감"],
}

POSITIVE_WORDS = ["좋", "만족", "깔끔", "편", "정확", "세련", "빠르", "예쁘", "탄탄", "실용"]
NEGATIVE_WORDS = ["아쉬", "작", "길", "부담", "비싸", "어둡", "얇", "까슬", "늦", "불안", "약해"]


def build_review_analysis(
    products: list[Product],
    reviews: list[Review],
    target_product_id: str = "A",
) -> tuple[ReviewAnalysisGroup, ReviewAnalysisGroup]:
    positioning = build_positioning(products, target_product_id)
    target_product = next((product for product in positioning.products if product.product_id == target_product_id), None)
    if target_product is None:
        target_product = positioning.products[0]
        target_product_id = target_product.product_id

    competitor_ids = [
        product.product_id
        for product in positioning.products
        if product.product_id != target_product_id and product.quadrant == target_product.quadrant
    ]

    target_reviews = [review for review in reviews if review.product_id == target_product_id]
    competitor_reviews = [review for review in reviews if review.product_id in competitor_ids]

    return (
        analyze_reviews(f"{target_product.brand} {target_product.product_id}", [target_product_id], target_reviews),
        analyze_reviews("동일 사분면 경쟁 상품", competitor_ids, competitor_reviews),
    )


def analyze_reviews(label: str, product_ids: list[str], reviews: list[Review]) -> ReviewAnalysisGroup:
    buckets = {
        category: {
            "positive": [],
            "negative": [],
            "neutral": [],
            "keywords": Counter(),
        }
        for category in CATEGORY_KEYWORDS
    }

    for review in reviews:
        categories = classify_categories(review.review_text)
        sentiment = classify_sentiment(review.review_text, review.rating)
        for category in categories:
            buckets[category][sentiment].append(review.review_text)
            for keyword in CATEGORY_KEYWORDS[category]:
                if keyword in review.review_text:
                    buckets[category]["keywords"][keyword] += 1

    insights = []
    for category, bucket in buckets.items():
        insights.append(
            CategoryInsight(
                category=category,
                positive_summary=summarize(category, bucket["positive"], "positive"),
                negative_summary=summarize(category, bucket["negative"], "negative"),
                keywords=[item[0] for item in bucket["keywords"].most_common(5)] or CATEGORY_KEYWORDS[category][:3],
                positive_count=len(bucket["positive"]),
                negative_count=len(bucket["negative"]),
                neutral_count=len(bucket["neutral"]),
            )
        )

    return ReviewAnalysisGroup(
        label=label,
        product_ids=product_ids,
        total_reviews=len(reviews),
        categories=insights,
    )


def classify_categories(text: str) -> list[str]:
    matched = [
        category
        for category, keywords in CATEGORY_KEYWORDS.items()
        if any(keyword in text for keyword in keywords)
    ]
    return matched or ["품질"]


def classify_sentiment(text: str, rating: int) -> str:
    positive_hits = sum(1 for word in POSITIVE_WORDS if word in text)
    negative_hits = sum(1 for word in NEGATIVE_WORDS if word in text)

    if rating >= 4 and positive_hits >= negative_hits:
        return "positive"
    if rating <= 3 and negative_hits >= positive_hits:
        return "negative"
    if positive_hits > negative_hits:
        return "positive"
    if negative_hits > positive_hits:
        return "negative"
    return "neutral"


def summarize(category: str, texts: list[str], sentiment: str) -> str:
    if not texts:
        return "관련 리뷰가 아직 충분하지 않습니다."

    word_counter = Counter()
    for text in texts:
        for keyword in CATEGORY_KEYWORDS[category]:
            if keyword in text:
                word_counter[keyword] += 1

    top_keyword = word_counter.most_common(1)[0][0] if word_counter else CATEGORY_KEYWORDS[category][0]
    if sentiment == "positive":
        return f"{top_keyword} 관련 만족 의견이 많고, 착용 경험을 긍정적으로 평가합니다."
    return f"{top_keyword} 관련 불편 의견이 확인되어 상세 개선 포인트로 관리가 필요합니다."
