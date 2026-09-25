import os

def load_inventory():
    inventory_total = 0
    history_list = []
    try:
        with open("inventory_report.txt", "r") as file:
            lines = file.readlines()
            if lines:
                inventory_total = int(lines[0].strip().split(":")[1])
                for line in lines[2:]:
                    parts = line.strip().split(", ")
                    quantity = int(parts[0].split(":")[1])
                    value = float(parts[1].split(":")[1].replace("$", ""))
                    tax = float(parts[2].split(":")[1].replace("$", ""))
                    history_list.append((quantity, value, tax))
    except FileNotFoundError:
        print("No existing inventory report found.")
    except ValueError:
        print("Error reading inventory report. Starting with empty inventory.")
    return inventory_total, history_list

def get_valid_input():
    user_input = input("Enter a stock quantity to add items, or 'quit' to exit: ").lower()
    if user_input == 'quit':
        return 'quit'
    try:
        quantity = int(user_input)
        if quantity < 0:
            print("Please enter a non-negative integer for quantity.")
            return None
        return quantity
    except ValueError:
        print("Please enter a valid integer for quantity.")
        return None
    
def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(delivery_value):
    return delivery_value * 0.1

def generate_report(total_units, failed_attempts):
    print("\nInventory Report:")
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected entries: {failed_attempts}")
    
def save_inventory(total, history):
    with open("inventory_report.txt", "w") as file:
        file.write(f"Final Inventory: {total}\n")
        file.write("Transaction History:\n")
        for entry in history:
            quantity, value, tax = entry
            file.write(f"Quantity: {quantity}, Value: ${value:.2f}, Tax: ${tax:.2f}\n")
    print("Inventory report saved to 'inventory_report.txt'.")
    
inventory, transaction_history = load_inventory()
rejected_entries = 0
deliveries_processed = 0
PRICE_PER_UNIT = 10.0
total_value = 0.0
total_tax = 0.0


while True:
    quantity = get_valid_input()
    
    if quantity == 'quit':
        generate_report(deliveries_processed, rejected_entries)
        save_inventory(inventory, transaction_history)
        break
    
    elif quantity is None:
        rejected_entries += 1

    else:
        inventory = process_delivery(inventory, quantity)
        
        delivery_value = quantity * PRICE_PER_UNIT
        tax = calculate_tax(delivery_value)
        
        transaction_history.append((quantity, delivery_value, tax))
        
        if inventory > 500:
            print("Warning: Inventory exceeds 500 items.")
            rejected_entries += 1
            save_inventory(inventory, transaction_history)
            generate_report(deliveries_processed, rejected_entries)
            break
        
        deliveries_processed += 1
        
        
        total_value += delivery_value
        total_tax += tax
        print(f"Added {quantity} items. Total inventory: {inventory}. Delivery value: ${delivery_value:.2f}, Tax: ${tax:.2f}")