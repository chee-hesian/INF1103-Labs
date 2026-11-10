from __future__ import annotations
from product import Product
from supplier import Supplier

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def get_fulfilment_info(self) -> str:
        return f"Delivered via digital download link ({self.__download_size}MB)."

    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self.__download_size}MB | Supplier: {self.get_supplier().get_name() if self.get_supplier() else 'N/A'}")
    
    def to_dict(self) -> dict:
        return {
            "type": "digital",
            "id": self.get_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock(),
            "download_size": self.__download_size,
            "supplier": {
                "supplier_id": self.get_supplier().get_id(),
                "name": self.get_supplier().get_name(),
                "contact_info": self.get_supplier().get_contact_info()
            } if self.get_supplier() else None
        }