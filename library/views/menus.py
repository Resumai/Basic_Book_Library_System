from library.context import SystemContext
from library.utils.snippets import clear
from library.actions.book_actions import (
    add_book, 
    remove_one_book, 
    remove_multiple_books, 
    search_multiple_books
    )



# User menu
def user_menu(ctx : SystemContext):
    book_inventory = ctx.book_inventory
    lend_records = ctx.lending_manager
    user_manager = ctx.user_manager

    print("\n--- User Menu ---")
    print("1. Show all books")
    print("2. Show all books borrowed")
    print("3. Borrow a book")
    print("4. Return a book")
    print("5. Search books by type")
    print("6. Logout")
    user_input = input("Enter your choice: ")
    clear()

    match user_input:
        case "1": book_inventory.print_all_books()
        case "2": lend_records.get_books_borrowed(user_manager.current_user)
        case "3":
            if lend_records.check_overdue_records(user_manager):
                print("You have overdue records. Please return them before borrowing a new book.")
                return
            book_inventory.print_all_books()
            try:
                user_input = int(input("Enter the number of the book to borrow: ")) -1
            except ValueError:
                print("Invalid input. Returning to user menu...")
                return
            lend_records.add_lend_record(user_input, user_manager, book_inventory)
            print("Book borrowed successfully.")
        case "4":
            lend_records.get_books_borrowed(user_manager.current_user)
            try:
                user_input = int(input("Enter the number of the book to return: ")) -1
            except ValueError:
                print("Invalid input. Returning to user menu...")
                return
            lend_records.remove_lend_record(user_input, user_manager, book_inventory)
            print("Book returned successfully.")
        case "5": search_multiple_books()
        case "6": user_manager.logout()
        case _: print("Invalid input.")


# Admin menu
def admin_menu(ctx : SystemContext):
    book_inventory = ctx.book_inventory
    lend_records = ctx.lending_manager
    user_manager = ctx.user_manager

    print("\n--- Admin Menu ---")
    print("1. Show all books")
    print("2. Search books by type")
    print("3. Add book")
    print("4. Remove one book")
    print("5. Remove multiple books")
    print("6. Get overdue books")
    print("7. Show all users")
    print("8. Create user")
    print("9. Remove user")
    print("0. Logout")

    try:
        user_input = input("Enter your choice: ")
    except ValueError:
        clear()
        print("Invalid input.")
        return
    clear()

    match user_input:
        case "1": book_inventory.print_all_books()
        case "2": search_multiple_books()
        case "3": add_book()
        case "4": remove_one_book()
        case "5": remove_multiple_books()
        case "6": print(lend_records.get_overdue_records())
        case "7": user_manager.print_users()
        case "8":
            username_input = input("Enter the username of the user to create: ")
            password_input = input("Enter the password of the user to create: ")
            if not username_input or not password_input:
                clear()
                print("Must enter username and password. Returning to admin menu...")
                return
            clear()
            user_manager.add_user(username_input, password_input)
        case "9":
            user_manager.print_users()
            user_input = input("Enter the card ID of the user to remove: ")
            print(user_manager.remove_user(user_input))
        case "0":
            user_manager.logout()
            return
        case _: print("Invalid input.")
        

# Login menu
def login_menu(ctx : SystemContext):
    user_manager = ctx.user_manager

    print("\n--- Login ---")
    print("Enter nothing to return to main menu.")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    clear()
    user_manager.login(username, password)

    if not username or not password:
        print("Must enter username and password. Returning to main menu...")
        return
    elif user_manager.current_user.role == "Admin":
        print("Successfully logged in as Admin.")
        while user_manager.current_user.role == "Admin":
            admin_menu(ctx)
    elif user_manager.current_user.role == "User":
        print(f"Successfully logged in as {user_manager.current_user.username}.")
        while user_manager.current_user.role == "User":
            user_menu(ctx)
    else:
        print("Incorrect username or password. Returning to main menu...")


# Main function
def main_menu(ctx : SystemContext):
    clear()

    while True:
        print("\n--- Welcome to the library system ---")
        print("1. Login")
        print("2. Exit")
        choice = input("Enter your choice: ")
        clear()

        match choice:
            case "1": login_menu(ctx)
            case "2":
                print("Have a good day!")
                break
            case _: print("Invalid input.")
