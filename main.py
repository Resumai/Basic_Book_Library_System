import os
from library import Book, BookInventory, LendingManager, UserManager



book_inventory = BookInventory()
user_manager = UserManager()
lend_records = LendingManager()







# Helper function to clear the screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()


# Adds a book to the inventory
def add_book():
    book_inventory.print_all_books()
    print("\n--- Add Book ---")
    try:        
        title = input("Enter the title of the book: ")
        author = input("Enter the author of the book: ")
        year = input("Enter the year of the book: ")
        genre = input("Enter the genre of the book: ")
        
        if not title or not author or not year or not genre:
            clear()
            print("Entered nothing for some fields. Returning to main menu...")
            return
        book_inventory.add_book(Book(title, author, int(year), genre))
    except ValueError:
        print("Invalid input. Returning to main menu...")
    print("Book added successfully.")


# Removes a book from the inventory
def remove_one_book():
    clear()
    book_inventory.print_all_books()
    print("\n--- Remove Book ---")
    user_input = input("Enter number of book to remove: ")

    try:
        del book_inventory[int(user_input)-1]
    except (ValueError, IndexError):
        print("Invalid book number. Returning to main menu...")
        return
    
    print("Book removed successfully.")


# Searches for books by attribute e.g. title, author, year, genre
# Doesnt do partial string searches - you need to enter the exact string
# Too tired to implement partial searches
def search_multiple_books():
    clear()
    print("\n--- Search Books by Type ---")
    print("1. Title")
    print("2. Author")
    print("3. Year")
    print("4. Genre")
    user_input = input("Enter your choice: ")

    results : dict[str, Book]
    match user_input:
        case "1":
            title = input("Enter the title of the books to search for: ")
            results = book_inventory.search_books_by_attr("title", title)
            for key in results:
                print(f"{key}. {results[key].title}")
        case "2":
            author = input("Enter the author of the books to search for: ")
            results = book_inventory.search_books_by_attr("author", author)
            for key in results:
                print(f"{key}. {results[key].author}")
        case "3":
            try:
                year_start = int(input("Enter the start year of the books to search for: "))
                year_last = int(input("Enter the last year of the books to search for: "))
            except ValueError:
                print("Invalid year. Returning to main menu...")
                return
            for year in range(year_start, year_last+1):
                results = book_inventory.search_books_by_attr("year", year)
                for key in results:
                    print(f'"{results[key].title}", By {results[key].author}, Year: {results[key].year}, Genre: {results[key].genre}, Index: {int(key)}')
        case "4":
            genre = input("Enter the genre of the books to search for: ")
            results = book_inventory.search_books_by_attr("genre", genre)
            for key in results:
                print(f"{key}. {results[key].genre}")
        case _: print("Invalid input. Returning to main menu...")


# Removes multiple books from the inventory
# Could have compressed this, but i think it's more readable this way, and was lazy.
def remove_multiple_books():
    clear()
    book_inventory.print_all_books()
    print("\n--- Remove Multiple Books ---")
    print("1. Remove by title")
    print("2. Remove by author")
    print("3. Remove by year")
    print("4. Remove by genre")
    user_input = input("Enter your choice: ")

    match user_input:
        case "1":
            title = input("Enter the title of the books to remove: ")
            book_inventory.remove_books_by_attr("title", title)
        case "2":
            author = input("Enter the author of the books to remove: ")
            book_inventory.remove_books_by_attr("author", author)
        case "3":
            try:
                year_start = int(input("Enter the start year of the books to remove: "))
                year_last = int(input("Enter the last year of the books to remove: "))
            except ValueError:
                print("Invalid year. Returning to admin menu...")
                return
            for year in range(year_start, year_last+1):
                book_inventory.remove_books_by_attr("year", year)
        case "4":
            genre = input("Enter the genre of the books to remove: ")
            book_inventory.remove_books_by_attr("genre", genre)
        case _: print("Invalid input. Returning to admin menu...")


# User menu
def user_menu():
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
def admin_menu():
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
def login_menu():
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
            admin_menu()
    elif user_manager.current_user.role == "User":
        print(f"Successfully logged in as {user_manager.current_user.username}.")
        while user_manager.current_user.role == "User":
            user_menu()
    else:
        print("Incorrect username or password. Returning to main menu...")


# Main function
def main():
    clear()

    while True:
        print("\n--- Welcome to the library system ---")
        print("1. Login")
        print("2. Exit")
        choice = input("Enter your choice: ")
        clear()

        match choice:
            case "1": login_menu()
            case "2":
                print("Have a good day!")
                break
            case _: print("Invalid input.")


main()


# For debugging purposes:
# from dev_stuff.snippets import print_all_user_data, print_lend_records, populate_mock_data

# populate_mock_data() # can populate mock data for fresh start, but first need to delete all files in data folder
# book_inventory.print_all_books()
# print_all_user_data()
# print(len(user_manager))
# print_lend_records()

# Admin credentials:
# username: Admin
# password: 1234

# User 1 credentials:
# username: 0001
# password: 0001

# User 2 credentials(for overdue test):
# username: 0002
# password: 0002

