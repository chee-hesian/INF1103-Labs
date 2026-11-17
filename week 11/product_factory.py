from __future__ import annotations
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier


class ProductFactory:
    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        weight: float = 0.0,
        download_size: float = 0.0,
    ) -> Product:
        normalized_type = product_type.strip().lower()
        if normalized_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, weight, supplier)
        elif normalized_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, download_size, supplier)
        else:
            raise ValueError(f"Unknown product type: {product_type}")