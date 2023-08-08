import sqlite3

from langchain import FAISS
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.embeddings import GPT4AllEmbeddings
from langchain.text_splitter import CharacterTextSplitter


class VectorDatabase:
    def __init__(self, embeddings=GPT4AllEmbeddings()):
        self.embeddings = embeddings

    def create_index(self, index_name, split_text):
        db = FAISS.from_documents(split_text, self.embeddings)
        db.save_local("faiss_db", index_name=index_name)

    def load_index(self, index_name):
        db = FAISS.load_local(
            "faiss_db", index_name=index_name, embeddings=self.embeddings
        )
        return db

    def split_text(self, loader, chunk_size=1000, chunk_overlap=0):
        text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        documents = text_splitter.split_documents(loader.load())
        return documents

    def add_txt(self, document_path):
        raw_documents = TextLoader(document_path)
        return self.split_text(raw_documents)

    def add_pdf(self, pdf_path):
        loader = PyPDFLoader(pdf_path)
        return self.split_text(loader)


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

