from __future__ import annotations
from order_line import OrderLine
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from product import Product

class Order:
    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
    
    def add_order_line(self, product: Product, quantity: int) -> None:
        """Add an orderline to the order."""
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)
    
    def calculate_total(self) -> float:
        """Calculate total cost for the order."""
        return sum(line.calculate_subtotal() for line in self.order_lines)    
    
    def display_order_summary(self) -> None:
        """Display a summary of the order."""
        print(f"Order ID: {self.order_id}")
        for line in self.order_lines:
            print(f"Product: {line.product.get_name()} | Quantity: {line.quantity} | Subtotal: ${line.calculate_subtotal():.2f}")
        print(f"Total Order Cost: ${self.calculate_total():.2f}")