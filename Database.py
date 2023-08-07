import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

from langchain.vectorstores import (
    Pinecone,
)
import sqlite3


class VectorDatabase:
    def __init__(self):
        load_dotenv()  # loads env variables
        pinecone.init(
            api_key=os.getenv("PINECONE_API_KEY"), environment="us-west1-gcp-free"
        )
        self.index_name = "bookindex"
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            disallowed_special=(),
        )
        self.model = ChatOpenAI(model_name="gpt-3.5-turbo")

    def add_to_index(self, documents):
        self.db = Pinecone.from_documents(
            documents,
            self.embeddings,
            index_name=self.index_name,
        )


class BookDatabase:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS books
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT,
                                author TEXT,
                                index_name TEXT)"""
        )
        self.conn.commit()

    def search_books(self, keyword):
        self.cursor.execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
            (f"%{keyword}%", f"%{keyword}%"),
        )
        rows = self.cursor.fetchall()

        # Convert the rows to dictionaries
        books = [dict(row) for row in rows]
        return books

    def add_book(self, title, author, index_name):
        # Check if the book already exists in the database
        self.cursor.execute(
            "SELECT * FROM books WHERE title = ? AND author = ?", (title, author)
        )
        existing_book = self.cursor.fetchone()
        if existing_book:
            print("Book already exists in the database.")
            return existing_book[0]  # Return the ID of the existing book

        # Insert the new book entry if it doesn't exist
        self.cursor.execute(
            "INSERT INTO books (title, author, index_name) VALUES (?, ?, ?)",
            (title, author, index_name),
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def delete_all_books(self):
        self.cursor.execute("DELETE FROM books")
        self.conn.commit()
        print("All books deleted.")

    def delete_book_by_id(self, book_id):
        self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.conn.commit()
        print(f"Book with ID {book_id} deleted.")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()


# Create an instance of the BookDatabase class
db = BookDatabase("books.db")

# Add a new book entry
book_id = db.add_book("The Great Gatsby", "F. Scott Fitzgerald", "index1")
# db.delete_all_books()
# Search for books
results = db.search_books("Gatsby")

# Print the search results
for book in results:
    print(book)

# Close the database connection
db.close_connection()
