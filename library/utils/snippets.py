from os import system, name

def clear():
    system('cls' if name == 'nt' else 'clear')



from library import Book, BookInventory, User, LendingManager, UserManager


book_inventory = BookInventory()
user_manager = UserManager()
lend_records = LendingManager()

def populate_mock_data():
    # make sure no data files in data folder exist
    from library.utils.mock_data import books_lib
    book_inventory.add_all_books(books_lib)
    user_manager.add_admin("Admin", "1234")
    user_manager.add_user("John", "0001")
    user_manager.add_user("Overdue Jack", "0002")
    user_manager.login("0002", "0002")
    lend_records.add_lend_record(15, user_manager, book_inventory, -28)
    user_manager.logout()


# Prints all books in the book inventory
def print_books():
    book : Book
    print("Books:")
    for x, book in enumerate(book_inventory):
        print(f"{x+1}. {book.title}")

def print_all_user_data():
    user : User
    print("Users:")
    for x, user in enumerate(user_manager):
        print(f"{x+1}. User: {user.username}, Card ID: {user.card_id}, Role: {user.role}, Password: {user.password}")
        print("Books borrowed:")
        for y, book in enumerate(user.books_borrowed):
            print(f"    {y+1}. Title: {book.title}, UUID: {book.uuid}")

def print_lend_records():
    print("Lend Records:")
    for x, record in enumerate(lend_records):
        print(f"{x+1}. Title: {record.book.title}, Book UUID: {record.book.uuid}, Reader: {record.user.username}, Reader UUID: {record.user.card_id}, Borrowed at: {record.borrowed_at}, Due date: {record.due_date}")