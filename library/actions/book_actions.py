from library.utils.snippets import clear
from library.managers.book_inventory import BookInventory
from library.models.book import Book



# Adds a book to the inventory
def add_book(book_inventory : BookInventory):
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
def remove_one_book(book_inventory : BookInventory):
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



# Removes multiple books from the inventory
# Could have compressed this, but i think it's more readable this way, and was lazy.
def remove_multiple_books(book_inventory : BookInventory):
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



# Searches for books by attribute e.g. title, author, year, genre
# Doesnt do partial string searches - you need to enter the exact string
# Too tired to implement partial searches
def search_multiple_books(book_inventory : BookInventory):
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