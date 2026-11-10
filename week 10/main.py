from __future__ import annotations
import json
import os

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, "inventory.json")

def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())

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

def save_inventory(inventory: Inventory, silent: bool = False) -> None:
    """Save the Inventory collection to inventory.json."""
    if not silent:
        print("Saving inventory...")
    data = [p.to_dict() for p in inventory.get_all_products()]
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)
    if not silent:
        print("Inventory saved successfully to inventory.json.")

def display_all_handler(inventory: Inventory) -> None:
    inventory.display_all()

def add_product_handler(inventory: Inventory) -> None:
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

def update_stock_handler(inventory: Inventory) -> None:
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

def search_product_handler(inventory: Inventory) -> None:
    print("\n--- Search Product ---")
    prod_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(prod_id)

    if product:
        print("Product Found:")
        show_product_details(product)
    else:
        print("Product not found.")
    
def remove_product_handler(inventory: Inventory) -> None:
    print("\n--- Remove Product ---")
    prod_id = input("Enter Product ID to remove: ").strip()
    if inventory.remove_product(prod_id):
        print(f"Product with ID '{prod_id}' removed successfully.")
    else:
        print(f"No product found with ID '{prod_id}'.")    
    
def run_menu(inventory: Inventory) -> None:
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
    inv = load_inventory()
    run_menu(inv)