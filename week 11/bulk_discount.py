from __future__ import annotations
from discount_strategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, discount_amount: float) -> None:
        self.__threshold: float = threshold
        self.__discount_amount: float = discount_amount

    def get_threshold(self) -> float:
        return self.__threshold

    def get_discount_amount(self) -> float:
        return self.__discount_amount

    def apply(self, total: float) -> float:
        return total - self.__discount_amount if total >= self.__threshold else total