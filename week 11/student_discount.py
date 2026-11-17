from __future__ import annotations
from discount_strategy import DiscountStrategy


class StudentDiscount(DiscountStrategy):
    def __init__(self, percentage: float = 5.0) -> None:
        self.__percentage: float = percentage

    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1.0 - self.__percentage / 100.0)