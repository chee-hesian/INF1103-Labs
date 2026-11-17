from __future__ import annotations
from typing import TYPE_CHECKING
from order_line import OrderLine
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount

if TYPE_CHECKING:
    from product import Product


class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def set_discount(self, discount: DiscountStrategy) -> None:
        """Change the discount strategy applied to this order."""
        self.discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Add an orderline to the order."""
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        """Calculate total cost for the order using the active discount strategy."""
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)

    def display_order_summary(self) -> None:
        """Display a summary of the order."""
        print(f"Order ID: {self.order_id}")
        for line in self.order_lines:
            print(f"Product: {line.product.get_name()} | Quantity: {line.quantity} | Subtotal: ${line.calculate_subtotal():.2f}")
        print(f"Total Order Cost: ${self.calculate_total():.2f}")