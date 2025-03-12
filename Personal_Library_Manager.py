import json
import streamlit as st

# Library Manager Class
class LibraryManager:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = self.load_books()

    def load_books(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_books(self):
        with open(self.filename, "w") as file:
            json.dump(self.books, file, indent=4)

    def add_book(self, title, author, year):
        self.books.append({"title": title, "author": author, "year": year})
        self.save_books()

    def remove_book(self, title):
        self.books = [book for book in self.books if book["title"] != title]
        self.save_books()

    def search_book(self, title):
        for book in self.books:
            if book["title"].lower() == title.lower():
                return book
        return None

    def list_books(self):
        return self.books


# Streamlit UI
st.title("📚 Personal Library Manager")

library = LibraryManager()

# Sidebar Menu
menu = st.sidebar.radio("Select an option", ["Add Book", "Remove Book", "Search Book", "List Books"])

if menu == "Add Book":
    st.header("➕ Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.text_input("Publication Year")

    if st.button("Add Book"):
        if title and author and year:
            library.add_book(title, author, year)
            st.success(f"✅ '{title}' added successfully!")
        else:
            st.warning("⚠️ Please fill in all fields.")

elif menu == "Remove Book":
    st.header("🗑 Remove a Book")
    title = st.text_input("Enter the book title to remove")

    if st.button("Remove Book"):
        library.remove_book(title)
        st.success(f"❌ '{title}' removed successfully!")

elif menu == "Search Book":
    st.header("🔎 Search for a Book")
    title = st.text_input("Enter the book title to search")

    if st.button("Search"):
        book = library.search_book(title)
        if book:
            st.success(f"✅ Found: **{book['title']}** by {book['author']} ({book['year']})")
        else:
            st.error("❌ Book not found.")

elif menu == "List Books":
    st.header("📖 List of Books")
    books = library.list_books()
    
    if books:
        for book in books:
            st.write(f"**{book['title']}** by {book['author']} ({book['year']})")
    else:
        st.warning("⚠️ No books in the library.")

