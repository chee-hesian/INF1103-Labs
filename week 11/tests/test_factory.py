from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from supplier import Supplier
from product_factory import ProductFactory


def run_factory_tests() -> None:
    print("=== SECTION 3.2: ProductFactory Creation & Error Handling ===")
    supplier = Supplier("SUP-01", "Global Logistics", "contact@global.com")

    phys = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, supplier, weight=1.2)
    dig = ProductFactory.create("digital", "D001", "Photo Editor", 49.90, 100, supplier, download_size=150.0)

    phys.display_information()
    print(phys.get_fulfilment_info())

    dig.display_information()
    print(dig.get_fulfilment_info())

    print("\nAttempting to create unsupported 'service' product:")
    try:
        ProductFactory.create("service", "S001", "Installation", 30.00, 5, supplier)
    except ValueError as err:
        print(f"Caught expected ValueError: {err}")


if __name__ == "__main__":
    run_factory_tests()