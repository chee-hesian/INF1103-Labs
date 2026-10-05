import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, "inventory.json")



def load_inventory():
    if os.path.exists(FILE_PATH):
        print("inventory.json file found. Loading inventory...")
        try:
            with open(FILE_PATH, "r") as file:
                inventory = json.load(file)
                print("Inventory loaded successfully.")
                return inventory
        except json.JSONDecodeError:
            print("Error: inventory.json is not a valid JSON file. Starting with an empty inventory.")
            return []
    else:
        print("inventory.json file not found. Starting with an empty inventory.")
        return []
    

def save_inventory(inventory, silent=False):
    """Save the inventory list to inventory.json."""
    if not silent:
        print("Saving inventory...")
    with open(FILE_PATH, "w") as file:
        json.dump(inventory, file, indent=4)
    if not silent:
        print("Inventory saved successfully to inventory.json.")


def display_all(inventory):
    print("Current Inventory")
    for item in inventory:
        print(
            f"ID: {item['id']} | Name: {item['name']} | "
            f"Price: ${item['price']:.2f} | Stock: {item['stock']}"
        )


def add_product(inventory):
    print("Add New Product")
    prod_id = input("Product ID: ").strip()

    for item in inventory:
        if item["id"].lower() == prod_id.lower():
            print("Product ID already exists.")
            return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
    except ValueError:
        print("Invalid numerical value.")
        return

    inventory.append({"id": prod_id, "name": name, "price": price, "stock": stock})
    print("Product added successfully!")


def update_stock(inventory):
    print("Update Stock")
    prod_id = input("Enter Product ID: ").strip()

    for item in inventory:
        if item["id"].lower() == prod_id.lower():
            print("Product Found:")
            print(f"Name: {item['name']}")
            print(f"Current Stock: {item['stock']}")
            try:
                new_stock = int(input("New Stock Quantity: ").strip())
                item["stock"] = new_stock
                print("Stock updated successfully!")
            except ValueError:
                print("Invalid stock number entered.")
            return

    print("Product not found.")


def search_product(inventory):
    print("Search Product")
    prod_id = input("Enter Product ID: ").strip()

    for item in inventory:
        if item["id"].lower() == prod_id.lower():
            print("Product Found")
            print(f"ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Price: ${item['price']:.2f}")
            print(f"Stock: {item['stock']}")
            return

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
        "1": display_all,
        "2": add_product,
        "3": update_stock,
        "4": search_product,
        "5": save_inventory,
    }

    action = actions.get(choice)
    if action:
        action(inventory)
    else:
        print("Invalid option. Please choose between 1 and 6.")

    return run_menu(inventory) 


print("INVENTORY MANAGEMENT SYSTEM")
inventory = load_inventory()
run_menu(inventory)