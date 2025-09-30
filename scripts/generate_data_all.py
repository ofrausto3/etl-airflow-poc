from pathlib import Path
import random, json, yaml
from datetime import datetime
import pandas as pd
from faker import Faker

fake = Faker()
N = 1000
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def gen_customers(n=N):
    rows = []
    for i in range(1, n+1):
        rows.append({
            "customer_id": i,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": f"user{i}@example.com",
            "phone": fake.numerify("###-###-####"),
            "city": fake.city(),
            "registration_date": fake.date_between(start_date="-2y", end_date="today").isoformat(),
            "customer_type": random.choice(["Regular", "Premium", "VIP"]),
        })
    return pd.DataFrame(rows)

def gen_products(n=N):
    rows = []
    for i in range(1, n+1):
        rows.append({
            "product_id": i,
            "product_name": f"Product {i}",
            "category": random.choice(["Electronics","Home","Sports","Beauty","Grocery"]),
            "brand": random.choice(["Acme","Globex","Umbrella","Initech","Soylent"]),
            "unit_price": round(random.uniform(5, 500), 2),
            "stock_quantity": random.randint(0, 1000),
            "is_active": random.choice([True, False]),
        })
    return pd.DataFrame(rows)

def gen_orders(n=N, max_customer_id=N):
    rows = []
    for i in range(1, n+1):
        rows.append({
            "order_id": i,
            "customer_id": random.randint(1, max_customer_id),
            "order_date": fake.date_time_between(start_date="-1y", end_date="now").isoformat(sep=" "),
            "order_status": random.choice(["Pending","Shipped","Delivered"]),
            "payment_method": random.choice(["Card","PayPal","Cash","ApplePay","GooglePay"]),
            "total_amount": round(random.uniform(10, 2000), 2),
            "discount_amount": round(random.uniform(0, 100), 2),
            "shipping_cost": round(random.uniform(0, 40), 2),
        })
    return pd.DataFrame(rows)

def write_all_formats(df: pd.DataFrame, base_name: str):
    (DATA_DIR / f"{base_name}.csv").write_text(df.to_csv(index=False), encoding="utf-8")
    df.to_json(DATA_DIR / f"{base_name}.json", orient="records", indent=2)
    with open(DATA_DIR / f"{base_name}.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(df.to_dict(orient="records"), f, sort_keys=False)

if __name__ == "__main__":
    customers = gen_customers()
    products  = gen_products()
    orders    = gen_orders(max_customer_id=len(customers))

    write_all_formats(customers, "customers")
    write_all_formats(products,  "products")
    write_all_formats(orders,    "orders")

    print("Generated 9 files in ./data ")
