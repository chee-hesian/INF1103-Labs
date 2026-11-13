from __future__ import annotations
from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight

    def get_weight(self) -> float:
        return self.__weight

    def calculate_shipping_cost(self) -> float:
        return 5.00 + (self.__weight * 2.00)

    def get_fulfilment_info(self) -> str:
        return f"Physical shipping required (Weight: {self.__weight}kg, Shipping Cost: ${self.calculate_shipping_cost():.2f})"

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.__weight}kg (Est. Shipping: ${self.calculate_shipping_cost():.2f}) | Supplier: {self.get_supplier().get_name() if self.get_supplier() else 'N/A'}")

    def to_dict(self) -> dict:
        return {
            "type": "physical",
            "id": self.get_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock(),
            "weight": self.__weight,
            "supplier": {
                "supplier_id": self.get_supplier().get_id(),
                "name": self.get_supplier().get_name(),
                "contact_info": self.get_supplier().get_contact_info()
            } if self.get_supplier() else None
        }