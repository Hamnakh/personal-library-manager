import json

class PersonalLibraryManager:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.library = self.load_library()

    def load_library(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                # Ensure the JSON is stored correctly as a dictionary
                if isinstance(data, dict) and "books" in data:
                    return data["books"]
                elif isinstance(data, list):  # If old format is detected
                    return data  # Assume it’s a list of books
                else:
                    return []  # Default empty list
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_library(self):
        with open(self.filename, "w") as file:
            json.dump({"books": self.library}, file, indent=4)

    def add_book(self):
        title = input("Enter the book title: ").strip()
        author = input("Enter the author: ").strip()
        try:
            year = int(input("Enter the publication year: "))
        except ValueError:
            print("Invalid year format. Please enter a valid number.")
            return
        genre = input("Enter the genre: ").strip()
        read_status = input("Have you read this book? (yes/no): ").strip().lower() == "yes"

        new_book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read_status
        }

        self.library.append(new_book)
        self.save_library()
        print("✅ Book added successfully!")

    def remove_book(self):
        title = input("Enter the title of the book to remove: ").strip().lower()
        initial_count = len(self.library)
        self.library = [book for book in self.library if book["title"].lower() != title]

        if len(self.library) < initial_count:
            self.save_library()
            print("✅ Book removed successfully!")
        else:
            print("❌ Book not found.")

    def search_book(self):
        choice = input("Search by:\n1. Title\n2. Author\nEnter your choice: ").strip()
        keyword = input("Enter the search term: ").strip().lower()

        results = [book for book in self.library if 
                   (choice == "1" and keyword in book["title"].lower()) or 
                   (choice == "2" and keyword in book["author"].lower())]

        if results:
            print("\n🔍 Matching Books:")
            for book in results:
                status = "✅ Read" if book["read"] else "📖 Unread"
                print(f"- {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
        else:
            print("❌ No matching books found.")

    def display_books(self):
        if not self.library:
            print("📚 Your library is empty.")
        else:
            print("\n📚 Your Library Collection:")
            for i, book in enumerate(self.library, 1):
                status = "✅ Read" if book["read"] else "📖 Unread"
                print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")

    def display_statistics(self):
        total_books = len(self.library)
        if total_books == 0:
            print("📉 No books in the library.")
            return

        read_books = sum(1 for book in self.library if book["read"])
        unread_books = total_books - read_books
        percentage_read = (read_books / total_books) * 100

        print("\n📊 Library Statistics:")
        print(f"📚 Total books: {total_books}")
        print(f"✅ Read books: {read_books}")
        print(f"📖 Unread books: {unread_books}")
        print(f"📈 Percentage read: {percentage_read:.2f}%")

    def menu(self):
        while True:
            print("\n📚 Welcome to the Personal Library Manager")
            print("1️⃣ Add a book")
            print("2️⃣ Remove a book")
            print("3️⃣ Search for a book")
            print("4️⃣ Display all books")
            print("5️⃣ Display statistics")
            print("6️⃣ Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.remove_book()
            elif choice == "3":
                self.search_book()
            elif choice == "4":
                self.display_books()
            elif choice == "5":
                self.display_statistics()
            elif choice == "6":
                self.save_library()
                print("💾 Library saved to file. Goodbye! 👋")
                break
            else:
                print("❌ Invalid choice. Please try again.")

# Corrected Main Entry Point
if __name__ == "__main__":
    manager = PersonalLibraryManager()
    manager.menu()

