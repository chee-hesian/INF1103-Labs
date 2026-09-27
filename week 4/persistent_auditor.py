import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_catalog():
    try:
        with open(os.path.join(SCRIPT_DIR, "catalog.json"), "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
        
def load_inventory():
    inventory_stock = {}
    history_list = []
    filepath = os.path.join(SCRIPT_DIR, "inventory.txt")

    if not os.path.exists(filepath):
        return inventory_stock, history_list

    current_section = None
    with open(filepath, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("Total Unique Items:") or line.startswith("Total Recorded Transactions:"):
                continue

            if line == "--- Current Stock Totals ---":
                current_section = "totals"
                continue
            elif line == "--- Transaction History Log ---":
                current_section = "history"
                continue

            parts = line.split(", ")
            if current_section == "totals" and len(parts) == 3:
                _, name, qty = parts[0], parts[1], int(parts[2])
                inventory_stock[name] = qty
            elif current_section == "history" and len(parts) == 3:
                history_list.append((parts[0], parts[1], int(parts[2])))
    
    return inventory_stock, history_list

def save_inventory(inventory_stock, history_list, catalog):
    filepath = os.path.join(SCRIPT_DIR, "inventory.txt")
    with open(filepath, "w") as file:

        file.write("--- Current Stock Totals ---\n")
        file.write(f"Total Unique Items: {len(inventory_stock)}\n")
        for item_name, qty in inventory_stock.items():
            item_id = catalog[item_name]["id"]
            file.write(f"{item_id}, {item_name}, {qty}\n")

        file.write("\n--- Transaction History Log ---\n")
        file.write(f"Total Recorded Transactions: {len(history_list)}\n")
        for entry in history_list:
            item_id, item_name, qty = entry
            file.write(f"{item_id}, {item_name}, {qty}\n")

    print("Order and transaction history successfully saved to inventory.txt")

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
        return matched_item, quantity
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

print("Current Orders:")
if inventory:
    for item_name, qty in inventory.items():
        item_id = catalog[item_name]["id"]
        print(f"{item_id}, {item_name}: {qty}")
else:
    print("No current orders.")
rejected_entries = 0
deliveries_processed = 0
total_value = 0.0
total_tax = 0.0


while True:
    item, quantity = get_valid_input(catalog)
    
    if item == 'quit':
        generate_report(deliveries_processed, rejected_entries)
        save_inventory(inventory, transaction_history, catalog)
        break
    
    elif quantity is None:
        rejected_entries += 1

    else:
        inventory[item] = process_delivery(inventory.get(item, 0), quantity)
        item_id = catalog[item]["id"]
        item_price = catalog[item]["price"]
        delivery_value = quantity * item_price
        tax = calculate_tax(delivery_value)
        
        transaction_history.append((item_id, item, quantity))
        
        print("\nNew Order Added:")
        print(f"{item_id}, {item}, {quantity}\n")
        
        if sum(inventory.values()) > 500:
            print("Warning: Inventory exceeds 500 items.")
            rejected_entries += 1
            generate_report(deliveries_processed, rejected_entries)
            save_inventory(inventory, transaction_history, catalog)
            break
        
        deliveries_processed += 1
        total_value += delivery_value
        total_tax += tax
        
        print(f"Added {quantity} items. Total inventory: {inventory}. Delivery value: ${delivery_value:.2f}, Tax: ${tax:.2f}")