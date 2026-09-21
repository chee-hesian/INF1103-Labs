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
    
inventory = 0
rejected_entries = 0
deliveries_processed = 0
PRICE_PER_UNIT = 10.0
total_value = 0.0
total_tax = 0.0

while True:
    quantity = get_valid_input()
    
    if quantity == 'quit':
        generate_report(deliveries_processed, rejected_entries)
        break
    
    elif quantity is None:
        rejected_entries += 1

    else:
        inventory = process_delivery(inventory, quantity)
        
        if inventory > 500:
            print("Warning: Inventory exceeds 500 items.")
            rejected_entries += 1
            generate_report(deliveries_processed, rejected_entries)
            break
        
        deliveries_processed += 1
        delivery_value = quantity * PRICE_PER_UNIT
        tax = calculate_tax(delivery_value)
        total_value += delivery_value
        total_tax += tax
        
        print(f"Added {quantity} items. Total inventory: {inventory}. Delivery value: ${delivery_value:.2f}, Tax: ${tax:.2f}")