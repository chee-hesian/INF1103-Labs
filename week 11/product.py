from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from supplier import Supplier

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    def get_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def update_stock(self, quantity: int) -> None:
        """Encapsulated method to update product stock."""
        self.__stock = quantity

    def display_information(self) -> None:
        """Display formatted individual product details."""
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}",
            end=" | "
        )
    
    def get_supplier(self) -> Supplier:
        return self.__supplier
        
    @abstractmethod
    def to_dict(self) -> dict:
        """Serialize Product to dictionary for JSON persistence."""
        pass

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Subclasses must define their fulfilment behavior."""
        pass