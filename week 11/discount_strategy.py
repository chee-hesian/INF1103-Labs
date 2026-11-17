from __future__ import annotations
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        """Apply discount logic to an order total and return the final amount."""
        pass