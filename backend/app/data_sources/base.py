from abc import ABC, abstractmethod

from app.schemas import Product, Review


class DataSource(ABC):
    @abstractmethod
    def get_products(self) -> list[Product]:
        """Return product records."""

    @abstractmethod
    def get_reviews(self) -> list[Review]:
        """Return review records."""
