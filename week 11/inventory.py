from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from product import Product

class Inventory:
    def __init__(self) -> None:
        self.products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """Adds a Product object if ID does not already exist."""
        if self.search_product(product.get_id()):
            return False
        self.products.append(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        """Finds and returns a Product object by ID (case-insensitive), or None."""
        for product in self.products:
            if product.get_id().lower() == product_id.lower():
                return product
        return None

    search_product = find_product  # Alias for backward compatibility
    
    def remove_product(self, product_id: str) -> bool:
        """Removes a Product object by ID (case-insensitive). Returns True if removed, False if not found."""
        product = self.search_product(product_id)
        if product:
            self.products.remove(product)
            return True
        return False

    def display_all(self) -> None:
        """Displays all products using each Product's display_information method."""
        print("Current Inventory")
        for product in self.products:
            product.display_information()

    def get_all_products(self) -> list[Product]:
        return self.products