inventory = 0
rejected_entries = 0

while True:
    user_input = input("Enter a stock quantity to add items, or 'quit' to exit: ").lower()
    if user_input == 'quit':
        print("Exiting the inventory auditor. Current inventory:", inventory, ", Rejected entries:", rejected_entries)
        break
    try:
        quantity = int(user_input)
        if quantity < 0:
            rejected_entries += 1
            print("Please enter a non-negative integer for quantity.")
            continue
        inventory += quantity
        if inventory > 500:
            print("Warning: Inventory exceeds 500 items.")
            rejected_entries += 1
            break
        print(f"Added {quantity} items. Total inventory: {inventory}")
    except ValueError:
        rejected_entries += 1
        print("Please enter a valid integer for quantity.")

        


        
        
        