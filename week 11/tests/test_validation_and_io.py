from __future__ import annotations
import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from supplier import Supplier
from inventory import Inventory
from order import Order
from product_factory import ProductFactory
from io_handlers import get_positive_float, load_products


def run_validation_and_io_tests() -> None:
    supplier = Supplier("SUP-01", "Global Logistics", "contact@global.com")

    # --- Section 4: Domain Validation ---
    print("=== SECTION 4: Domain Validation Checks ===")
    for label, fn in [
        ("Zero price", lambda: ProductFactory.create("physical", "P99", "Bad Price", 0.0, 5, supplier)),
        ("Negative stock", lambda: ProductFactory.create("digital", "D99", "Bad Stock", 10.0, -1, supplier)),
        ("Zero order quantity", lambda: Order("ORD-99").add_order_line(
            ProductFactory.create("physical", "P01", "Valid Item", 10.0, 5, supplier), 0
        )),
    ]:
        try:
            fn()
        except ValueError as err:
            print(f"[{label}] Rejected with ValueError: {err}")

    # --- Section 5.1: get_positive_float() ---
    print("\n=== SECTION 5.1: get_positive_float() Simulation ('abc', '-5', '12.50') ===")
    with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
        result = get_positive_float("Enter price: ")
    print(f"Returned value: {result} (type: {type(result).__name__})")

    # --- Section 5.2: load_products() with valid CSV ---
    print("\n=== SECTION 5.2A: load_products() with products.csv ===")
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "products.csv"))
    inv = Inventory()
    load_products(csv_path, inv, supplier)
    inv.display_all()

    # --- Section 5.2B: load_products() with missing CSV ---
    print("\n=== SECTION 5.2B: load_products() with missing file ===")
    missing_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "missing_products.csv"))
    inv_empty = Inventory()
    load_products(missing_path, inv_empty, supplier)


if __name__ == "__main__":
    run_validation_and_io_tests()