from main import Supplier, PhysicalProduct, Order

def run_composition_test():
    print("=== TEST: Composition Lifecycle (Section 4.3) ===")

    # 1. Create a single product with a supplier
    supplier = Supplier("SUP-01", "Keychron", "support@keychron.com")
    keyboard = PhysicalProduct("P101", "Mechanical Keyboard", 120.00, 20, 0.9, supplier)

    # 2. Create two distinct orders
    order1 = Order("ORD-001")
    order2 = Order("ORD-002")

    # 3. Add the same product to both orders
    order1.add_order_line(keyboard, quantity=2)
    order2.add_order_line(keyboard, quantity=1)

    print("\n--- Order 1 Details ---")
    for idx, line in enumerate(order1.order_lines, 1):
        print(f"Line {idx}: {line.product.get_name()} | Qty: {line.quantity} | Subtotal: ${line.calculate_subtotal():.2f}")
    print(f"Order 1 Total: ${order1.calculate_total():.2f}")

    print("\n--- Order 2 Details ---")
    for idx, line in enumerate(order2.order_lines, 1):
        print(f"Line {idx}: {line.product.get_name()} | Qty: {line.quantity} | Subtotal: ${line.calculate_subtotal():.2f}")
    print(f"Order 2 Total: ${order2.calculate_total():.2f}")

    # 4. Identity & Reference Verifications (Predictions)
    print("\n--- Identity Comparisons ---")
    same_line = order1.order_lines[0] is order2.order_lines[0]
    same_product = order1.order_lines[0].product is order2.order_lines[0].product

    print(f"Are the OrderLine objects the same instance? {same_line}")
    print(f"Are the underlying Product objects the same instance? {same_product}")
    print(f"OrderLine 1 ID: {hex(id(order1.order_lines[0]))}")
    print(f"OrderLine 2 ID: {hex(id(order2.order_lines[0]))}")
    print(f"Keyboard Product ID: {hex(id(keyboard))}")

if __name__ == "__main__":
    run_composition_test()