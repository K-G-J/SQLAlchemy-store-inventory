from models import (Base, engine)
from lib.csv_actions import add_csv, backup_db
from lib.db_actions import add_product, delete_product, update_promt, view_product


# Main menu options
def menu():
    while True:
        print('''
              \rPRODUCTS
              \r- Enter "v" to view the details of a product
              \r- Enter "a" to add a new product
              \r- Enter "u" to update a product
              \r- Enter "d" to delete a product
              \r- Enter "b" to backup the entire contents of the database
              \r- Enter "e" to exit''')
        choice = (input('What would you like to do?  ')).lower()
        if choice in ['v', 'a', 'u', 'd', 'b', 'e']:
            return choice
        else:
            while input('''
                  \r❗️Please choose one of the options above.❗️
                  \rInput "v", "a", "u", "d", "b", or "e"
                  \rPress ENTER to try again.''') != "":
                continue


def app():
    add_csv()
    app_running = True
    while app_running:
        choice = menu()
        if choice == "v":
            # View the details of a product
            view_product()
        elif choice == "a":
            # Add a new product
            add_product()
        elif choice == "u":
            # Update a product
            update_promt()
        elif choice == "d":
            # Delete a product
            delete_product()
        elif choice == "b":
            # Backup the entire contents of the database
            backup_db()
        else:
            print("\nThank you for using the store inventory database.\nGoodbye 👋\n")
            app_running = False
            return


if __name__ == '__main__':
    Base.metadata.create_all(engine)  # Connect to the database
    app()
