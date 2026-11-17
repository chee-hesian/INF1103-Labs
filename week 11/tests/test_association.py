from main import Supplier, PhysicalProduct, DigitalProduct

def run_association_test():
    print("=== TEST 1: Association Lifecycle (Section 2.2) ===")
    
    # 1. Instantiate an independent Supplier object
    supplier = Supplier("S001", "Global Logistics", "contact@global.com")
    
    # 2. Pass the Supplier instance to both Product types
    phys_prod = PhysicalProduct("P01", "Ergonomic Chair", 199.99, 10, 8.5, supplier)
    dig_prod = DigitalProduct("D01", "Chair 3D Model", 29.99, 50, 15.0, supplier)
    
    # 3. Action: Delete the local variable reference
    print("\nExecuting: del supplier")
    del supplier
    
    # 4. Verify products still retain valid references to the supplier
    print("\n--- Physical Product ---")
    phys_prod.display_information()
    print()
    print("Supplier info retrieved via PhysicalProduct:")
    phys_prod.get_supplier().display_information()
    print(f"Supplier object memory address: {hex(id(phys_prod.get_supplier()))}")
    
    print("\n--- Digital Product ---")
    dig_prod.display_information()
    print()
    print("Supplier info retrieved via DigitalProduct:")
    dig_prod.get_supplier().display_information()
    print(f"Supplier object memory address: {hex(id(dig_prod.get_supplier()))}")
    
    # 5. Confirm both products share the exact same Supplier instance
    same_instance = phys_prod.get_supplier() is dig_prod.get_supplier()
    print(f"\nDo both products point to the same Supplier instance? {same_instance}")

if __name__ == "__main__":
    run_association_test()