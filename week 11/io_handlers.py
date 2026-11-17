from __future__ import annotations
import csv
from inventory import Inventory
from supplier import Supplier
from product_factory import ProductFactory


def get_positive_float(prompt: str) -> float:
    """Prompt the user repeatedly until a valid float greater than zero is entered."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Load products from a CSV file using ProductFactory and add valid rows to Inventory."""
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip header row
            loaded = 0
            for row_num, row in enumerate(reader, start=2):
                if len(row) < 5:
                    print(f"Row {row_num} skipped: incomplete data {row}")
                    continue
                try:
                    p_type = row[0].strip()
                    p_id = row[1].strip()
                    name = row[2].strip()
                    price = float(row[3].strip())
                    stock_qty = int(row[4].strip())
                    product = ProductFactory.create(p_type, p_id, name, price, stock_qty, supplier)
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as err:
                    print(f"Row {row_num} skipped ({row}): {err}")
                    continue
            print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")