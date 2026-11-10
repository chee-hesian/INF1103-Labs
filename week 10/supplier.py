from __future__ import annotations

class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_info: str = contact_email
        
    def get_id(self) -> str:
        return self.__supplier_id
    
    def get_name(self) -> str:
        return self.__name
    
    def get_contact_info(self) -> str:
        return self.__contact_info

    def display_information(self) -> None:
        """Display formatted supplier details."""
        print(
            f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | Contact: {self.__contact_info}"
        )