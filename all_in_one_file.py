import os
import pickle
import uuid
from datetime import timedelta, date


## This whole project in a single file. Only thing needed is data files.

# --- Book Class ---
class Book:
    def __init__(self, title : str, author : str, year : int, genre : str):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.uuid = self.generate_uid()

    def __str__(self):
        return f"Title: {self.title}, UUID: {self.uuid}"
    
    def __repr__(self):
        return str(self.__dict__)

    def generate_uid(self):
        return str(uuid.uuid4())


# --- BookInventory Class ---
class BookInventory:
    def __init__(self, inventory_file=r"data\inventory.pkl"):
        self.inventory_file = inventory_file
        self.book_inventory : list[Book] = self._load_inventory()
    
    # returns an iterator for the inventory, useful for for loops
    def __iter__(self):
        return iter(self.book_inventory)
    
    # returns the number of books in the inventory, useful for len()
    def __len__(self): 
        return len(self.book_inventory)
    
    # returns the book at the index in the inventory, useful for indexing
    def __getitem__(self, index): 
        return self.book_inventory[index]

    # index is the index of the book in the inventory, book is the new book, 
    # useful for assigning a new book to an existing index
    def __setitem__(self, index, book): 
        if not isinstance(book, Book):
            raise ValueError("Invalid value")
        self.book_inventory[index] = book

    # returns True if the book is in the inventory, useful for in operator
    def __contains__(self, book): 
        return book in self.book_inventory

    # removes a book from the inventory, based on the index
    def __delitem__(self, index):
        del self.book_inventory[index]

    def save_inventory(self):
        with open(self.inventory_file, "wb") as f:
            pickle.dump(self.book_inventory, f)

    def _load_inventory(self):
        if os.path.exists(self.inventory_file):
            with open(self.inventory_file, "rb") as f:
                return pickle.load(f)
        return []

    # adds all books from the list to the inventory
    def add_all_books(self, book_lst):
        for book in book_lst:
            self.add_book(Book(book["title"], book["author"], book["year"], book["genre"]))

    # adds a book to the inventory
    def add_book(self, book):
        self.book_inventory.append(book)
        self.save_inventory()

     # removes a book from the inventory, based on the book object
    def remove_book(self, book):
        self.book_inventory.remove(book)
        self.save_inventory()

    # removes books from the inventory, based on the object attribute e.g. title, author, year, genre
    def remove_books_by_attr(self, attr, value):
        new_inventory = []
        for book in self.book_inventory:
            if getattr(book, attr) != value:
                new_inventory.append(book)
        self.book_inventory = new_inventory
        #OR vodoo magic:
        # self.book_inventory = [
        #     book for book in self.book_inventory if getattr(book, attr) != value
        # ]
        self.save_inventory()

    # searches for books by attribute e.g. title, author, year, genre
    def search_books_by_attr(self, attr, value):
        results = {}
        for x, book in enumerate(self.book_inventory):
            if getattr(book, attr) == value:
                results[f"{x+1}"] = book
        return results
    
    # prints all books in the inventory
    def print_all_books(self):
        print("\n--- All books ---")
        for x, book in enumerate(self.book_inventory):
            print(f'{str(x+1) + ".":<3}' 
                  f'{'"'+ book.title +'"':<70}'
                  f'By {book.author:<45}'
                  f'Year: {book.year:<6} Genre: {book.genre}')
        print("--- End of list ---")


# --- User Class ---
class User:
    def __init__(self, username = None, password = None, card_id = None, role = None ):
        self.username = username
        self.password = password
        self.card_id = card_id
        self.role = role
        self.books_borrowed : list[Book] = []

        if role == "Admin":
            self.login_id = username # username is the login id for admins
        elif role == "User":
            self.login_id = card_id # card_id is the login id for users

    def __str__(self):
        return f"User : {self.username}"

    def __iter__(self):
        return iter(self.books_borrowed)
    
    def __getitem__(self, index):
        return self.books_borrowed[index]

    def borrow_book(self, book):
        self.books_borrowed.append(book)

    def remove_borrowed_book(self, book):
        self.books_borrowed.remove(book)


# --- LendingRecord Class ---
class LendingRecord:
    def __init__(self, book: Book, user: User, duration_days: int = 14, borrowed_at = None):
        self.book = book
        self.user = user
        self.borrowed_at = borrowed_at if borrowed_at else date.today()
        self.due_date = self.borrowed_at + timedelta(days=duration_days)

    def __str__(self):
        return f"{self.book.title} by {self.book.author} borrowed by {self.user.username} on {self.borrowed_at} due on {self.due_date}"

    # checks if the lend record is overdue
    def is_overdue(self):
        return date.today() > self.due_date


# --- UserManager Class ---
class UserManager:
    def __init__(self, users_file=r"data\users.pkl"):
        self.users_file = users_file
        self.users : dict[str, User] = self._load_users()
        self.current_user : User  = User()

    def __iter__(self):
        return iter(self.users.values())
    
    def __len__(self):
        return len(self.users)

    def __getitem__(self, index):
        return self.users[index]

    def _get_unused_id(self):
        if self.users == {}:
            return "0000"
        else:
            max_id = 0
            for user in self.users.values():
                if int(user.card_id) > max_id:
                    max_id = int(user.card_id)
            new_id = max_id + 1
            return f"{new_id:04d}"

    
    def save_users(self):
        with open(self.users_file, "wb") as file:
            pickle.dump(self.users, file)


    def _load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, "rb") as file:
                return pickle.load(file)
        return {}
    
    # updates the user
    def update_user(self):
        key = self.current_user.login_id
        self.users[key] = self.current_user
        self.save_users()

    # authenticates the user
    def authenticate(self, login_id : str, password):
        user = self.users.get(login_id)
        if user and user.password == password:
            return user
        return False
    
    # adds an admin to the system
    def add_admin(self, username_input, password_input):
        # generates unique id for admin, mb he will need to take some books or smth?
        card_id = self._get_unused_id()
        
        user = User(username_input, password_input, card_id, role = "Admin")
        self.users[username_input] = user
        self.save_users()
        return f"Admin added successfully: Login/Username ID: {username_input}, Password: {password_input}"

    # adds a user to the system
    def add_user(self, username_input, password_input):
        card_id = self._get_unused_id() # generates unique id for user
        user = User(username_input, password_input, card_id, role = "User")
        self.users[card_id] = user
        self.save_users()
        return f"User added successfully: Login/Card ID: {card_id}, Password: {password_input}"

    # removes a user from the system
    def remove_user(self, card_id_input):
        try:
            if self.users[card_id_input].role == "Admin":
                return f"Admin with card ID {card_id_input} cannot be removed."
        except KeyError:
            return f"User with card ID {card_id_input} not found."
        del self.users[card_id_input]
        self.save_users()
        return f"User with card ID {card_id_input} removed successfully."

    # prints all users in the system
    def print_users(self):
        for user in self.users.values():
            if user.role == "Admin":
                print(f"User: {user.username}, Card ID: {user.card_id}, Role: {user.role}")
            else:
                print(f"User: {user.username}, Card ID: {user.card_id}, Role: {user.role}, Password: {user.password}")

    # logs in a user
    def login(self, login_id, password):
        user = self.authenticate(login_id, password)
        if user:
            self.current_user = user
            return True
        return False

    def logout(self):
        self.current_user = User()


# --- LendingManager Class ---
class LendingManager:
    def __init__(self, lend_records_file=r"data\lend_records.pkl"):
        self.lend_records_file = lend_records_file
        self.lend_records : list[LendingRecord] = self.load_lend_records()

    def __str__(self):
        return f"Lending Manager: {self.lend_records} lend records"

    def __iter__(self):
        return iter(self.lend_records)

    def __len__(self):
        return len(self.lend_records)

    def save_lend_records(self):
        with open(self.lend_records_file, "wb") as f:
            pickle.dump(self.lend_records, f)

    def load_lend_records(self):
        if os.path.exists(self.lend_records_file):
            with open(self.lend_records_file, "rb") as f:
                return pickle.load(f)
        return []

    # Adds a lend record to the lend_records list
    def add_lend_record(self, user_input : int, user_manager : UserManager, book_inventory : BookInventory, duration_days=14):
        try:    
            book_to_borrow = book_inventory[user_input]
        except IndexError:
            return f"Book not found in inventory. Returning to user menu..."

        user_manager.current_user.borrow_book(book_to_borrow)
        book_inventory.remove_book(book_to_borrow)
        user_manager.update_user()

        loan_record = LendingRecord(book_to_borrow, user_manager.current_user, duration_days)
        self.lend_records.append(loan_record)
        self.save_lend_records()
        return f"Book borrowed successfully. Returning to user menu..."

    # Removes a lend record from the lend_records list
    def remove_lend_record(self, user_input : int , user_manager : UserManager, book_inventory : BookInventory):
        try:
            book_to_return = user_manager.current_user.books_borrowed[user_input]
        except IndexError:
            print("Book not found in lend records. Returning to user menu...")
            return False
        for loan in self.lend_records:
            if loan.book.uuid == book_to_return.uuid:
                user_manager.current_user.remove_borrowed_book(book_to_return)
                book_inventory.add_book(book_to_return)
                user_manager.update_user()
                self.lend_records.remove(loan)
                self.save_lend_records()
                return True

    # Checks if the current user has overdue records
    def check_overdue_records(self, user_manager: UserManager):
        for record in self.lend_records:
            if record.is_overdue() and record.user.card_id == user_manager.current_user.card_id:
                return True
        return False

    # Gets the due date of a book
    def get_due_date(self, book : Book):
        for record in self.lend_records:
            if record.book.uuid == book.uuid:
                return record.due_date
        return None

    # Gets all overdue records
    def get_overdue_records(self):
        record : LendingRecord
        overdue_records = []
        for record in self.lend_records:
            if record.is_overdue():
                overdue_records.append(
                    f"{record.book.title} by {record.book.author} | Borrowed by: {record.user.username} card ID: {record.user.card_id} | Due: {record.due_date}")
        return overdue_records

    # Gets all books borrowed by the current user
    def get_books_borrowed(self, current_user : User):
        if not current_user.books_borrowed:
            print("No books borrowed.")
            return
        for index, book in enumerate(current_user.books_borrowed):
            print(f"{index+1}. {book.title} by {book.author}, Due: {self.get_due_date(book)}")


# --- Main ---
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



# from dev_stuff.snippets import populate_mock_data, print_all_user_data, print_lend_records
# populate_mock_data() # can populate mock data for fresh start, butneed to delete all files in data folder:

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