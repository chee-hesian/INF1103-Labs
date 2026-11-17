from __future__ import annotations
import os
import sys

# Ensure parent directory is on sys.path when running from project root or tests/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from supplier import Supplier
from physical_product import PhysicalProduct
from order import Order
from bulk_discount import BulkDiscount
from percentage_discount import PercentageDiscount
from student_discount import StudentDiscount


def run_strategy_tests() -> None:
    supplier = Supplier("SUP-01", "Keychron Logistics", "support@keychron.com")
    monitor = PhysicalProduct("P100", "27-inch Monitor", 250.00, 10, 4.5, supplier)

    # --- Section 2.3: Strategy Switching ---
    print("=== SECTION 2.3: DiscountStrategy Switching ===")
    order1 = Order("ORD-101", discount=BulkDiscount(200, 20))
    order1.add_order_line(monitor, quantity=1)
    print(f"Total with BulkDiscount(200, 20): ${order1.calculate_total():.2f}")

    order1.set_discount(PercentageDiscount(10))
    print(f"Total after set_discount(PercentageDiscount(10)): ${order1.calculate_total():.2f}")

    # --- Section 2.4: Extending Without Modifying Order & Shared Strategy ---
    print("\n=== SECTION 2.4: StudentDiscount & Shared Strategy Instance ===")
    shared_pct_discount = PercentageDiscount(10)
    order2 = Order("ORD-102", discount=shared_pct_discount)
    order3 = Order("ORD-103", discount=shared_pct_discount)
    order2.add_order_line(monitor, quantity=1)
    order3.add_order_line(monitor, quantity=2)

    print(f"Order 2 Total (10% off $250): ${order2.calculate_total():.2f}")
    print(f"Order 3 Total (10% off $500): ${order3.calculate_total():.2f}")
    print(f"Do order2 and order3 share the same discount instance? {order2.discount is order3.discount}")

    student_order = Order("ORD-104", discount=StudentDiscount())
    student_order.add_order_line(monitor, quantity=1)
    print(f"Student Order Total (5% off $250): ${student_order.calculate_total():.2f}")


if __name__ == "__main__":
    run_strategy_tests()