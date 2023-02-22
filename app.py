from models import (Base, Product, session, engine)
import datetime
import csv
import time


# Main menu options
def menu():
    while True:
        print('''
              \nPRODUCTS
              \r- Enter "v" to view the details of a product
              \r- Enter "a" to add a new product
              \r- Enter "b" to backup the entire contents of the database
              \r- Enter "e" to exit''')
        choice = input('What would you like to do?  ')
        if choice in ['v', 'a', 'b', 'e']:
            return choice
        else:
            while input('''
                  \rPlease choose one of the options above.
                  \rInput "v", "a", "b", or "e"
                  \rPress enter to try again.''') != "":
                continue


def clean_price(price_str):
    try:
        price_float = float(price_str.replace('$', ''))
    except ValueError:
        while input("""
              \n❗️***** PRICE ERROR *****❗️
              \rThe price should be a number without a currency symbol.
              \rEx: 10.99
              \rPress enter to try again.
              \r*************************""") != "":
            continue
    else:
        return int(price_float * 100)


def clean_date(date_str):
    split_date = date_str.split('/')
    try:
        return_date = datetime.date(
            int(split_date[2]), int(split_date[0]), int(split_date[1]))
    except ValueError:
        while input("""
              \n❗️***** DATE ERROR *****❗️
              \rThe date format should include a valid Month Day, Year from the past.
              \rEx: 1/13/2022
              \rPress enter to try again.
              \r*************************""") != "":
            continue
        return
    else:
        return return_date


# Add products in inventory.csv
def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data)  # skip header row
        for row in data:
            product_in_db = session.query(Product).filter(
                Product.product_name == row[0]).one_or_none()
            if product_in_db == None:
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = int(row[2])
                date_updated = clean_date(row[3])
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
            print('\nPlease enter either "y" or "n"')
    else:
        return id_options


# Get and display a product by its product_id
def view_product():
    products = read_db()
    valid_ids = prompt_ids()
    while True:
        try:
            id = int(input("\nPlease enter a product ID:  "))
            if id not in valid_ids:
                print(f'\n{id} is not a valid product ID')
                prompt_ids()
        except ValueError as err:
            print(f'\nThat is not a valid ID\n({err})')
            prompt_ids()
            continue
        else:
            for product in products:
                if product['id'] == id:
                    print(f"""
                        \rName: {product['name']}
                        \rPrice: ${product['price'] / 100}
                        \rQuantity: {product['quantity']}
                        \rDate Updated: {product['date_updated']}
                        """)
                    return


def app():
    add_csv()
    app_running = True
    while app_running:
        choice = menu()
        if choice == "v":
            # view the details of a product
            pass
        elif choice == "a":
            # add a new product
            pass
        elif choice == "b":
            # backup the entire contents of the database
            pass
        else:
            print("Thank you for using the inventory database.\nGoodbye👋")
            app_running = False
            return


if __name__ == '__main__':
    # Connect to the database
    Base.metadata.create_all(engine)
    # app()
    view_product()
