from decimal import Decimal
import datetime


# Format product_price for database
def clean_price(price_str):
    try:
        price_float = Decimal(price_str.replace('$', ''))
    except ValueError:
        while input("""
              \n❗️***** PRICE ERROR *****❗️
              \rThe price should be a number without a currency symbol.
              \rEx: 10.99
              \rPress ENTER to try again.
              \r*************************""") != "":
            continue
    else:
        return int(price_float * 100)


# Format date_updated for database
def clean_date(date_str):
    try:
        split_date = date_str.split('/')
        return_date = datetime.date(
            int(split_date[2]), int(split_date[0]), int(split_date[1]))
        # TODO: fix this check
        if return_date > datetime.datetime.now():
            print('\nPlease enter a date from the past')
    except (ValueError, IndexError):
        while input("""
              \n❗️***** DATE ERROR *****❗️
              \rThe date format should include a valid Month, Day, and Year from the past.
              \rEx: 1/13/2022
              \rPress ENTER to try again.
              \r*************************""") != "":
            continue
        return
    else:
        return return_date


# Format product_quantity for database
def clean_quantity(quantity_str):
    try:
        product_quantity = int(quantity_str)
    except ValueError:
        while input("""
              \n❗️***** QUANTITY ERROR *****❗️
              \rThe product quantity should be a valid number.
              \rPress ENTER to try again.
              \r*************************""") != "":
            continue
        return
    else:
        return product_quantity