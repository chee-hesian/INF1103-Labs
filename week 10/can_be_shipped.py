from __future__ import annotations
from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Contract for calculating shipping charges."""
        pass