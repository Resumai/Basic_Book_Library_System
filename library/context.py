from library.managers.book_inventory import BookInventory
from library.managers.user_manager import UserManager
from library.managers.lending_manager import LendingManager



class SystemContext:
    def __init__(self):
        self.book_inventory = BookInventory()
        self.user_manager = UserManager()
        self.lending_manager = LendingManager()