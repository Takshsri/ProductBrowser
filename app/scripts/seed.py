from faker import Faker
from datetime import datetime,timedelta
import random
import uuid

from app.database import sessionLocal
from app.models import Product

fake = Faker()

TOTAL_PRODUCTS = 200000
BATCH_SIZE = 5000
categories = [
    "Electronics",
    "Fashion",
    "Books",
    "Sports",
    "Home",
    "Toys",
    "Beauty",
    "Automotive"
]

def generate_batch(size):
    products = []

    for _ in range(size):
        created_at = fake.date_time_between(
            start_date="-2y",
            end_date="now"
        )
        updated_at = created_at + timedelta(
            days = random.randint(0,30)
        )

        products.append({
            "id":str(uuid.uuid4()),
            "name":fake.catch_phrase(),
            "category":random.choice(categories),
            "created_at":created_at,
            "updated_at":updated_at
        })
    return products

def seed_products():
    db = sessionLocal()
    try:
        inserted = 0
        while inserted <TOTAL_PRODUCTS:
            batch_size = min(BATCH_SIZE,TOTAL_PRODUCTS - inserted)
            batch = generate_batch(batch_size)
            db.bulk_insert_mappings(
                Product,
                batch
            )
            db.commit()

            inserted += batch_size
            print(f"inserted{inserted}/{TOTAL_PRODUCTS}")
        print("Successfully inserted products")
    except Exception as e:
        db.rollback()
        print("Error:",e)
    finally:
        db.close()

if __name__ == "__main__":
    seed_products()
