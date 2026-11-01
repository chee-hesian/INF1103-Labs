import json
import os
from abc import ABC, abstractmethod

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, "inventory.json")

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Contract for calculating shipping charges."""
        pass

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

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
        
    @abstractmethod
    def to_dict(self) -> dict:
        """Serialize Product to dictionary for JSON persistence."""
        pass

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Subclasses must define their fulfilment behavior."""
        pass

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def get_weight(self) -> float:
        return self.__weight

    def calculate_shipping_cost(self) -> float:
        return 5.00 + (self.__weight * 2.00)

    def get_fulfilment_info(self) -> str:
        return f"Physical shipping required (Weight: {self.__weight}kg, Shipping Cost: ${self.calculate_shipping_cost():.2f})"

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.__weight}kg (Est. Shipping: ${self.calculate_shipping_cost():.2f})")

    def to_dict(self) -> dict:
        return {
            "type": "physical",
            "id": self.get_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock(),
            "weight": self.__weight
        }

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def get_fulfilment_info(self) -> str:
        return f"Delivered via digital download link ({self.__download_size}MB)."

    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self.__download_size}MB")
    
    def to_dict(self) -> dict:
        return {
            "type": "digital",
            "id": self.get_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock(),
            "download_size": self.__download_size
        }       
        
class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product: Product) -> bool:
        """Adds a Product object if ID does not already exist."""
        if self.search_product(product.get_id()):
            return False
        self.__products.append(product)
        return True

    def search_product(self, prod_id: str):
        """Finds and returns a Product object by ID (case-insensitive), or None."""
        for product in self.__products:
            if product.get_id().lower() == prod_id.lower():
                return product
        return None

    def display_all(self) -> None:
        """Displays all products using each Product's display_information method."""
        print("Current Inventory")
        for product in self.__products:
            product.display_information()

    def get_all_products(self):
        return self.__products

def load_inventory() -> Inventory:
    inventory = Inventory()
    if os.path.exists(FILE_PATH):
        print("inventory.json file found. Loading inventory...")
        try:
            with open(FILE_PATH, "r") as file:
                raw_data = json.load(file)
                for item in raw_data:
                    p_type = item.get("type", "physical")
                    if p_type == "physical":
                        product = PhysicalProduct(
                            item["id"],
                            item["name"],
                            float(item["price"]),
                            int(item["stock"]),
                            float(item.get("weight", 0.0))
                        )
                    elif p_type == "digital":
                        product = DigitalProduct(
                            item["id"],
                            item["name"],
                            float(item["price"]),
                            int(item["stock"]),
                            float(item.get("download_size", 0.0))
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
    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
        if type_choice == "1":
            weight = float(input("Weight (kg): ").strip())
            new_prod = PhysicalProduct(prod_id, name, price, stock, weight)
        else:
            download_size = float(input("Download Size (MB): ").strip())
            new_prod = DigitalProduct(prod_id, name, price, stock, download_size)
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
        product.display_information()
        print(f"Fulfilment Info: {product.get_fulfilment_info()}")
    else:
        print("Product not found.")
    
def run_menu(inventory):
    print("\nMENU")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")

    choice = input("Enter option: ").strip()

    if choice == "6":
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
    "5": save_inventory,
    }

    action = actions.get(choice)
    if action:
        action(inventory)
    else:
        print("Invalid option. Please choose between 1 and 6.")

    return run_menu(inventory) 

if __name__ == "__main__":
    print("INVENTORY MANAGEMENT SYSTEM")
    inventory = load_inventory()
    run_menu(inventory)