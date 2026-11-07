from __future__ import annotations
import json
import os
from abc import ABC, abstractmethod

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, "inventory.json")

def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Contract for calculating shipping charges."""
        pass

class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self.product: Product = product
        self.quantity: int = quantity
    
    def calculate_subtotal(self) -> float:
        """Calculate subtotal for this orderline."""
        return self.product.get_price() * self.quantity
    
class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.order_lines: list[OrderLine] = []
    
    def add_order_line(self, product: Product, quantity: int) -> None:
        """Add an orderline to the order."""
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)
    
    def calculate_total(self) -> float:
        """Calculate total cost for the order."""
        return sum(line.calculate_subtotal() for line in self.order_lines)    
    
    def display_order_summary(self) -> None:
        """Display a summary of the order."""
        print(f"Order ID: {self.order_id}")
        for line in self.order_lines:
            print(f"Product: {line.product.get_name()} | Quantity: {line.quantity} | Subtotal: ${line.calculate_subtotal():.2f}")
        print(f"Total Order Cost: ${self.calculate_total():.2f}")
    
class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.__supplier_id = supplier_id
        self.__name = name
        self.__contact_info = contact_email
        
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

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__supplier = supplier

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

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float, supplier: Supplier):
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight = weight

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

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float, supplier: Supplier):
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size = download_size

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
        
class Inventory:
    def __init__(self):
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

    def get_all_products(self):
        return self.products

def load_inventory() -> Inventory:
    inventory = Inventory()
    if os.path.exists(FILE_PATH):
        print("inventory.json file found. Loading inventory...")
        try:
            with open(FILE_PATH, "r") as file:
                raw_data = json.load(file)
                for item in raw_data:
                    p_type = item.get("type", "physical")
                    
                    supp_data = item.get("supplier", {})
                    supplier = Supplier(
                        supp_data.get("supplier_id", "SUP-DEFAULT"),
                        supp_data.get("name", "Standard Supplies"),
                        supp_data.get("contact_info", "supplier@example.com")
                    )
                    if p_type == "physical":
                        product = PhysicalProduct(
                            item["id"],
                            item["name"],
                            float(item["price"]),
                            int(item["stock"]),
                            float(item.get("weight", 0.0)),
                            supplier
                        )
                    elif p_type == "digital":
                        product = DigitalProduct(
                            item["id"],
                            item["name"],
                            float(item["price"]),
                            int(item["stock"]),
                            float(item.get("download_size", 0.0)),
                            supplier
                        )
                    else:
                        continue
                    inventory.add_product(product)
                print("Inventory loaded successfully.")
        except json.JSONDecodeError:
            print("Error: inventory.json is not a valid JSON file. Starting with an empty inventory.")
    else:
        print("inventory.json file not found. Starting with an empty inventory.")
    return inventory


def save_inventory(inventory: Inventory, silent=False):
    """Save the Inventory collection to inventory.json."""
    if not silent:
        print("Saving inventory...")
    data = [p.to_dict() for p in inventory.get_all_products()]
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)
    if not silent:
        print("Inventory saved successfully to inventory.json.")


def display_all_handler(inventory: Inventory):
    inventory.display_all()


def add_product_handler(inventory: Inventory):
    print("\n--- Add New Product ---")
    print("Select Product Type:")
    print("1. Physical Product")
    print("2. Digital Product")
    type_choice = input("Enter choice (1/2): ").strip()

    if type_choice not in ("1", "2"):
        print("Invalid product type selected.")
        return

    prod_id = input("Product ID: ").strip()
    if inventory.search_product(prod_id):
        print("Product ID already exists.")
        return

    name = input("Product Name: ").strip()
    
    supp_id = input("Supplier ID: ").strip()
    supp_name = input("Supplier Name: ").strip()
    supp_email = input("Supplier Contact Email: ").strip()
    supplier = Supplier(supp_id, supp_name, supp_email)
    
    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
        if type_choice == "1":
            weight = float(input("Weight (kg): ").strip())
            new_prod = PhysicalProduct(prod_id, name, price, stock, weight, supplier)
        else:
            download_size = float(input("Download Size (MB): ").strip())
            new_prod = DigitalProduct(prod_id, name, price, stock, download_size, supplier)
    except ValueError:
        print("Invalid numerical value entered.")
        return

    inventory.add_product(new_prod)
    print("Product added successfully!")


def update_stock_handler(inventory: Inventory):
    print("Update Stock")
    prod_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(prod_id)

    if product:
        print("Product Found:")
        print(f"Name: {product.get_name()}")
        print(f"Current Stock: {product.get_stock()}")
        try:
            new_stock = int(input("New Stock Quantity: ").strip())
            product.update_stock(new_stock)
            print("Stock updated successfully!")
        except ValueError:
            print("Invalid stock number entered.")
    else:
        print("Product not found.")


def search_product_handler(inventory: Inventory):
    print("\n--- Search Product ---")
    prod_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(prod_id)

    if product:
        print("Product Found:")
        show_product_details(product)
    else:
        print("Product not found.")
    
def remove_product_handler(inventory: Inventory):
    print("\n--- Remove Product ---")
    prod_id = input("Enter Product ID to remove: ").strip()
    if inventory.remove_product(prod_id):
        print(f"Product with ID '{prod_id}' removed successfully.")
    else:
        print(f"No product found with ID '{prod_id}'.")    
    
def run_menu(inventory):
    print("\nMENU")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Remove Product")
    print("6. Save Inventory")
    print("7. Exit")

    choice = input("Enter option: ").strip()

    if choice == "7":
        print("Saving inventory before exit...")
        save_inventory(inventory, silent=True)
        print("Inventory saved successfully.")
        print("Thank you for using Inventory Management System.")
        print("Program terminated.")
        return

    actions = {
    "1": display_all_handler,
    "2": add_product_handler,
    "3": update_stock_handler,
    "4": search_product_handler,
    "5": remove_product_handler,
    "6": save_inventory,
    }

    action = actions.get(choice)
    if action:
        action(inventory)
    else:
        print("Invalid option. Please choose between 1 and 7.")

    return run_menu(inventory) 

if __name__ == "__main__":
    print("INVENTORY MANAGEMENT SYSTEM")
    inventory = load_inventory()
    run_menu(inventory)