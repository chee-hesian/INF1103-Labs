import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_catalog():
    try:
        with open(os.path.join(SCRIPT_DIR, "catalog.json"), "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        {}
        
def load_inventory():
    inventory_stock = {}
    history_list = []
    filepath = os.path.join(SCRIPT_DIR, "inventory.txt")

    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if not line or line.startswith("Total Deliveries:"):
                    continue
                parts = line.split(", ")
                if len(parts) == 4:
                    item, qty, val, tax = parts[0], int(parts[1]), float(parts[2]), float(parts[3])
                    history_list.append((item, qty, val, tax))
                    inventory_stock[item] = inventory_stock.get(item, 0) + qty
    except FileNotFoundError:
        pass
    
    return inventory_stock, history_list

def get_valid_input(catalog):
    item_input = input("Enter product name or ID to add items, or 'quit' to exit: ").strip()
    if item_input.lower() == 'quit':
        return 'quit', None
    
    matched_item = None
    for item_name, details in catalog.items():
        if item_input.lower() == item_name.lower() or item_input == details.get("id"):
            matched_item = item_name
            break
    if not matched_item:
        print("Item not found in catalog.")
        return None, None
    
    user_input = input(f"Enter quantity for {matched_item}: ").strip()
    try:
        quantity = int(user_input)
        if quantity < 0:
            print("Please enter a non-negative integer for quantity.")
            return None, None
        return quantity, matched_item
    except ValueError:
        print("Please enter a valid integer for quantity.")
        return None, None
    
def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(delivery_value):
    return delivery_value * 0.1

def generate_report(total_units, failed_attempts):
    print("\nInventory Report:")
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected entries: {failed_attempts}")
    
catalog = load_catalog()    
if not catalog:
    print("Error: 'catalog.json' file not found or is not a valid JSON. Exiting program.")
    exit()
inventory, transaction_history = load_inventory()
print("Initial Inventory:", inventory)
rejected_entries = 0
deliveries_processed = 0


while True:
    item, quantity = get_valid_input(catalog)
    
    if item == 'quit':
        generate_report(deliveries_processed, rejected_entries)
        print(f"\n[Verification] Recorded transactions in memory ({len(transaction_history)} entries):")
        for record in transaction_history:
            print("  ", record)
        break
    
    elif quantity is None:
        rejected_entries += 1

    else:
        inventory[item] = process_delivery(inventory.get(item, 0), quantity)
        item_price = catalog[item]["price"]
        delivery_value = quantity * item_price
        tax = calculate_tax(delivery_value)
        
        transaction_history.append((item, quantity, delivery_value, tax))
        
        if sum(inventory.values()) > 500:
            print("Warning: Inventory exceeds 500 items.")
            rejected_entries += 1
            generate_report(deliveries_processed, rejected_entries)
            print(f"\n[Verification] Recorded transactions in memory ({len(transaction_history)} entries):")
            for record in transaction_history:
                print("  ", record)
            break
        
        deliveries_processed += 1
        total_value += delivery_value
        total_tax += tax
        
        print(f"Added {quantity} items. Total inventory: {inventory}. Delivery value: ${delivery_value:.2f}, Tax: ${tax:.2f}")