from main import Supplier, PhysicalProduct, Inventory

def run_aggregation_test():
    print("=== TEST 2: Aggregation Lifecycle (Section 3.2) ===")
    
    # 1. Create Product independently before adding to any Inventory
    supplier = Supplier("S001", "Apex Tech", "sales@apextech.com")
    laptop = PhysicalProduct("P01", "Gaming Laptop", 1899.99, 5, 2.3, supplier)
    
    inv_a = Inventory()
    inv_b = Inventory()
    
    # 2. Add product to Inventory A
    print("\n[Step 1] Adding laptop to Inventory A...")
    inv_a.add_product(laptop)
    inv_a.display_all()
    
    # 3. Remove product from Inventory A
    print("\n[Step 2] Removing laptop from Inventory A...")
    removed = inv_a.remove_product("P01")
    print(f"Removal successful: {removed}")
    
    print("\nInventory A contents after removal:")
    inv_a.display_all()
    
    # 4. Verify product remains intact in memory
    print("\n[Step 3] Verifying product object functions independently:")
    laptop.display_information()
    print(f"\nFulfilment: {laptop.get_fulfilment_info()}")
    print(f"Product object address: {hex(id(laptop))}")
    
    # 5. Transfer product to Inventory B
    print("\n[Step 4] Adding same product instance to Inventory B...")
    inv_b.add_product(laptop)
    inv_b.display_all()
    
    # 6. Verify identity
    retrieved = inv_b.find_product("P01")
    print(f"\nIs retrieved object in Inventory B identical to laptop? {retrieved is laptop}")

if __name__ == "__main__":
    run_aggregation_test()