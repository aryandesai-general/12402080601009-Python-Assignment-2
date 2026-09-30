"""Q9: Inventory objects with merge operator overloading.

Input format used here:
n m
then n lines for inventory A and m lines for inventory B:
product_id name stock purchase_price selling_price
Then q, followed by commands:
ADD A|B id name stock purchase selling
DELETE A|B id
UPDATE A|B id stock
MERGE
COMPARE
"""
from dataclasses import dataclass
import sys


@dataclass
class Product:
    product_id: str
    name: str
    stock: int
    purchase_price: float
    selling_price: float

    @property
    def value(self):
        return self.stock * self.selling_price


class Inventory:
    def __init__(self, products=()):
        self.products = {p.product_id: p for p in products}

    def add(self, product):
        if product.product_id in self.products:
            raise ValueError("Product ID already exists")
        self.products[product.product_id] = product

    def delete(self, product_id):
        if product_id not in self.products:
            raise ValueError("Unknown product ID")
        del self.products[product_id]

    def update(self, product_id, stock):
        if product_id not in self.products or stock < 0:
            raise ValueError("Unknown product or invalid stock")
        self.products[product_id].stock = stock

    @property
    def total_value(self):
        return sum(p.value for p in self.products.values())

    def __add__(self, other):
        merged = {key: Product(**vars(value)) for key, value in self.products.items()}
        for key, product in other.products.items():
            if key in merged:
                old = merged[key]
                old.stock += product.stock
                old.purchase_price = min(old.purchase_price, product.purchase_price)
                old.selling_price = max(old.selling_price, product.selling_price)
            else:
                merged[key] = Product(**vars(product))
        return Inventory(merged.values())

    def show(self):
        for p in sorted(self.products.values(), key=lambda p: p.product_id):
            print(f"{p.product_id} {p.name} stock={p.stock} "
                  f"purchase={p.purchase_price:g} selling={p.selling_price:g}")
        print(f"TOTAL_VALUE {self.total_value:g}")


def read_products(count):
    products = []
    for _ in range(count):
        pid, name, stock, purchase, selling = sys.stdin.readline().split()
        stock, purchase, selling = int(stock), float(purchase), float(selling)
        if stock < 0 or purchase < 0 or selling < 0:
            raise ValueError("Negative stock/price")
        products.append(Product(pid, name, stock, purchase, selling))
    return products


def main():
    try:
        n, m = map(int, sys.stdin.readline().split())
        a, b = Inventory(read_products(n)), Inventory(read_products(m))
        q = int(sys.stdin.readline())
        if n < 0 or m < 0 or q < 0:
            raise ValueError
    except (ValueError, TypeError):
        print("Invalid inventory input."); return

    merged = None
    for _ in range(q):
        parts = sys.stdin.readline().split()
        if not parts: continue
        try:
            command = parts[0].upper()
            if command == "ADD" and len(parts) == 7:
                inv = a if parts[1].upper() == "A" else b
                inv.add(Product(parts[2], parts[3], int(parts[4]), float(parts[5]), float(parts[6])))
                print("OK")
            elif command == "DELETE" and len(parts) == 3:
                (a if parts[1].upper() == "A" else b).delete(parts[2]); print("OK")
            elif command == "UPDATE" and len(parts) == 4:
                (a if parts[1].upper() == "A" else b).update(parts[2], int(parts[3])); print("OK")
            elif command == "MERGE":
                merged = a + b; merged.show()
            elif command == "COMPARE":
                print("A" if a.total_value > b.total_value else "B" if b.total_value > a.total_value else "EQUAL")
            else:
                raise ValueError("Invalid operation")
        except (ValueError, IndexError) as exc:
            print("ERROR", exc)


if __name__ == "__main__":
    main()
