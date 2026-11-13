from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from product import Product

class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        self.product: Product = product
        self.quantity: int = quantity
    
    def calculate_subtotal(self) -> float:
        """Calculate subtotal for this orderline."""
        return self.product.get_price() * self.quantity