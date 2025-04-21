
from datetime import timedelta, date
from library.models.book import Book
from library.models.user import User

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





    


