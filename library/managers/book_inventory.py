from ..models.book import Book
import pickle
import os


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

        