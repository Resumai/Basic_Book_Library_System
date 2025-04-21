from library.models.book import Book

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

    
