from ..models.book import Book
from .book_inventory import BookInventory
from ..models.lending_record import LendingRecord
from .user_manager import UserManager
from ..models.user import User
import pickle
import os


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