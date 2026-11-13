from main import Supplier, PhysicalProduct, DigitalProduct, Inventory, show_product_details

def run_test():
    print("=== TEST: LSP & Polymorphism (Sections 6 & 7) ===")

    supplier = Supplier("S001", "Global Logistics", "contact@global.com")
    keyboard = PhysicalProduct("P01", "Mechanical Keyboard", 100.0, 10, 1.5, supplier)
    guide = DigitalProduct("D01", "Python Guide", 25.0, 50, 45.0, supplier)

    # 1. Test LSP substitutability
    print("\n--- 1. Testing Subtype Substitutability (LSP) ---")
    print("Calling show_product_details with PhysicalProduct:")
    show_product_details(keyboard)

    print("\nCalling show_product_details with DigitalProduct:")
    show_product_details(guide)

    # 2. Test Polymorphism through Inventory
    print("\n--- 2. Testing Polymorphism via Inventory Collection ---")
    inv = Inventory()
    inv.add_product(keyboard)
    inv.add_product(guide)

    for product in inv.products:
        product.display_information()
        print(f"Fulfilment Info: {product.get_fulfilment_info()}")

if __name__ == "__main__":
    run_test()