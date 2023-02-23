from models import Product, session
from lib.clean_data import clean_date, clean_price
import csv
import time


# Add products in inventory.csv
def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data)  # skip header row
        for row in data:
            product_name = row[0]
            product_price = clean_price(row[1])
            product_quantity = int(row[2])
            date_updated = clean_date(row[3])
            duplicates = session.query(Product).filter(
                Product.product_name == product_name).all()
            if duplicates:
                for item in duplicates:
                    if date_updated > item.date_updated:
                        item.product_name = product_name
                        item.product_price = product_price
                        item.product_quantity = product_quantity
                        item.date_updated = date_updated
            else:
                new_product = Product(product_name=product_name, product_quantity=product_quantity,
                                      product_price=product_price, date_updated=date_updated)
                session.add(new_product)
            session.commit()


# Read products from the db
def read_db():
    products = []
    for product in session.query(Product):
        products.append({
            "id": product.product_id,
            "name": product.product_name,
            "price": product.product_price,
            "quantity": product.product_quantity,
            "date_updated": product.date_updated
        })
    return products


# Backup the database (Export new CSV)
def backup_db():
    products = read_db()
    writer = csv.writer(open('backup.csv', 'w'))
    writer.writerow(['product_name', 'product_price',
                    'product_quantity', 'date_updated'])
    for product in products:
        formatted_price = f"${product['price'] / 100:.2f}"
        formatted_date = f"{product['date_updated'].month}/{product['date_updated'].day}/{product['date_updated'].year}"
        writer.writerow([product['name'], formatted_price,
                        str(product['quantity']), formatted_date])
    print("\nDatabase backedup! ✅")
    time.sleep(1.5)
