import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_FILE = os.path.join(BASE_DIR, "products.json")
ORDERS_FILE = os.path.join(BASE_DIR, "orders.json")


def load_products():
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_order(order):
    orders = []
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            try:
                orders = json.load(f)
            except Exception:
                orders = []
    orders.append(order)
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def format_price(p):
    return f"{p:,.2f}"


def main():
    products = load_products()
    cart = {}

    while True:
        print("\n=== ร้านขายของ (CLI) ===")
        print("1) แสดงสินค้า")
        print("2) เพิ่มสินค้าเข้าตะกร้า")
        print("3) ดูตะกร้า")
        print("4) ลบสินค้าจากตะกร้า")
        print("5) ชำระเงิน / Checkout")
        print("6) ออกจากโปรแกรม")
        choice = input("เลือกเมนู: ").strip()

        if choice == "1":
            print("\n--- สินค้าที่มี ---")
            for pid, item in products.items():
                print(f"{pid}) {item['name']} — ราคา: {format_price(item['price'])} บาท (มี: {item.get('stock', 'N/A')})")

        elif choice == "2":
            pid = input("รหัสสินค้าที่จะเพิ่ม: ").strip()
            if pid not in products:
                print("รหัสสินค้าไม่ถูกต้อง")
                continue
            qty_s = input("จำนวน: ").strip()
            try:
                qty = int(qty_s)
                if qty <= 0:
                    raise ValueError()
            except ValueError:
                print("จำนวนไม่ถูกต้อง")
                continue
            cart[pid] = cart.get(pid, 0) + qty
            print("เพิ่มเรียบร้อย")

        elif choice == "3":
            print("\n--- ตะกร้าสินค้า ---")
            if not cart:
                print("ตะกร้าว่าง")
                continue
            total = 0.0
            for pid, qty in cart.items():
                item = products[pid]
                subtotal = item['price'] * qty
                total += subtotal
                print(f"{pid}) {item['name']} x{qty} = {format_price(subtotal)} บาท")
            print(f"รวมทั้งหมด: {format_price(total)} บาท")

        elif choice == "4":
            if not cart:
                print("ตะกร้าว่าง")
                continue
            pid = input("รหัสสินค้าที่จะลบ: ").strip()
            if pid not in cart:
                print("สินค้าไม่อยู่ในตะกร้า")
                continue
            del cart[pid]
            print("ลบเรียบร้อย")

        elif choice == "5":
            if not cart:
                print("ตะกร้าว่าง")
                continue
            name = input("ชื่อลูกค้า: ").strip()
            addr = input("ที่อยู่ (ไม่บังคับ): ").strip()
            total = 0.0
            items = []
            for pid, qty in cart.items():
                item = products[pid]
                subtotal = item['price'] * qty
                total += subtotal
                items.append({"id": pid, "name": item['name'], "qty": qty, "unit_price": item['price'], "subtotal": subtotal})
            order = {
                "customer": name,
                "address": addr,
                "items": items,
                "total": total
            }
            save_order(order)
            cart = {}
            print(f"ชำระเงินเรียบร้อย รวม {format_price(total)} บาท — คำสั่งซื้อถูกบันทึก")

        elif choice == "6":
            print("ลาก่อน!")
            break

        else:
            print("คำสั่งไม่ถูกต้อง")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nยกเลิกโดยผู้ใช้")
        sys.exit(0)
