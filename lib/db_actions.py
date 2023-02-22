from lib.clean_data import clean_date, clean_price, clean_quantity
from lib.csv_actions import read_db
from models import (Product, session)
from sqlalchemy import func
import datetime
import time


# Display products with their IDs
def prompt_ids():
    products = read_db()
    id_options = []
    for product in products:
        id_options.append(product['id'])
    while (see_ids := (input("\nWould you like to see all product IDs? (y/n)  ")).lower()) != "n":
        if see_ids == "y":
            for product in products:
                print(f"\n{product['id']}: {product['name']}")
            return id_options
        else:
            print('\n❗️ Please enter either "y" or "n"')
    else:
        return id_options


# Get selected product_id
def get_id():
    valid_ids = prompt_ids()
    while True:
        try:
            id = int(input("\nPlease enter a product ID:  "))
            if id not in valid_ids:
                print(f'\n❗️ {id} is not a valid product ID')
                prompt_ids()
                continue
        except ValueError as err:
            print(f'\n❗️ That is not a valid ID\n({err})')
            prompt_ids()
            continue
        else:
            return id


# Get and display a product by its product_id
def view_product():
    products = read_db()
    id = get_id()
    for product in products:
        if product['id'] == id:
            print(f"""
                \rName: {product['name']}
                \rPrice: ${product['price'] / 100:.2f}
                \rQuantity: {product['quantity']}
                \rDate Updated: {product['date_updated']}
                """)
            time.sleep(1.5)
            return


# Adding a product to the database
def add_product():
    existing_product = False
    products = read_db()
    product_name = input('\nProduct Name:  ')
    for product in products:
        if product['name'].lower() == product_name.lower():
            print(f'\n{product_name} already exists and will be updated')
            product = session.query(Product).filter(func.lower(
                Product.product_name).contains(func.lower(product_name))).first()
            product_id = product.product_id
            existing_product = True
    quantity_error = True
    while quantity_error:
        product_quantity = input('\nProduct Quantity:  ')
        product_quantity = clean_quantity(product_quantity)
        if type(product_quantity) == int:
            quantity_error = False
    price_error = True
    while price_error:
        product_price = input('\nPrice (Ex: 25.64):  ')
        product_price = clean_price(product_price)
        if type(product_price) == int:
            price_error = False
    date_error = True
    while date_error:
        date_updated = input('\nDate Updated (Ex: 10/25/2022):  ')
        date_updated = clean_date(date_updated)
        if type(date_updated) == datetime.date:
            date_error = False
    if existing_product:
        update_product(product_id, product_name, product_quantity,
                       product_price, date_updated)
    else:
        new_product = Product(product_name=product_name, product_quantity=product_quantity,
                              product_price=product_price, date_updated=date_updated)
        session.add(new_product)
        session.commit()
        print('\nProduct added! ✅')
        time.sleep(1.5)


# Prompt for product to update
def update_promt():
    id = get_id()
    product = session.query(Product).filter(
        Product.product_id == id).one()
    print(f'\nUpdating {product.product_name}')
    product_name = input('\nProduct Name:  ')
    quantity_error = True
    while quantity_error:
        product_quantity = input('\nProduct Quantity:  ')
        product_quantity = clean_quantity(product_quantity)
        if type(product_quantity) == int:
            quantity_error = False
    price_error = True
    while price_error:
        product_price = input('\nPrice (Ex: 25.64):  ')
        product_price = clean_price(product_price)
        if type(product_price) == int:
            price_error = False
    date_error = True
    while date_error:
        date_updated = input('\nDate Updated (Ex: 10/25/2022):  ')
        date_updated = clean_date(date_updated)
        if type(date_updated) == datetime.date:
            date_error = False
    update_product(id, product_name, product_quantity,
                   product_price, date_updated)


# Update existing product
def update_product(id, name, quantity, price, date_updated):
    product = session.query(Product).filter(
        Product.product_id == id).one()
    product.product_name = name
    product.product_quantity = quantity
    product.product_price = price
    product.date_updated = date_updated
    session.commit()
    print('\n{name} updated! ✅')
    time.sleep(1.5)


# Delete a product
def delete_product():
    id = get_id()
    product = session.query(Product).filter(
        Product.product_id == id).one()
    session.delete(product)
    session.commit()
    print('\n{product.product_name} deleted! ✅')
    time.sleep(1.5)
