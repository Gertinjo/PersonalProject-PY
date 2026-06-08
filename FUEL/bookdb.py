import sqlite3
from model import Book, BookCreate


def create_connection():
    """Creates a connection to the SQLite database."""
    connection = sqlite3.connect("book.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    """Creates the books table in the database if it doesn't exist."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()


def create_table_recipes():
    """Creates the recipes table in the database if it doesn't exist."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()


# Initialize the database table
create_table()


def create_book(book: BookCreate) -> int:
    """Adds a new book to the database."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (book.title, book.author))
    connection.commit()
    book_id = cursor.lastrowid
    connection.close()
    return book_id


def read_books():
    """Retrieves all books from the database."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    connection.close()
    books = [Book(id=row[0], title=row[1], author=row[2]) for row in rows]
    return books


def read_book(book_id: int):
    """Retrieves a single book from the database by its ID."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return None
    return Book(id=row["id"], title=row["title"], author=row["author"])


def update_book(book_id: int, book: BookCreate) -> bool:
    """Updates an existing book in the database."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE books SET title = ?, author = ? WHERE id = ?", (book.title, book.author, book_id))
    connection.commit()
    updated = cursor.rowcount
    connection.close()
    return updated > 0


def delete_book(book_id: int) -> bool:
    """Deletes a book from the database by its ID."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    connection.commit()
    deleted = cursor.rowcount
    connection.close()
    return deleted > 0
