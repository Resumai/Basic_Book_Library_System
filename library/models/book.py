import uuid

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