from fastapi import FastAPI, HTTPException
from typing import List
import bookdb
import model
from model import Book, BookCreate

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Books CRUD API"}

@app.post("/Books/", response_model=Book)
def create_book(book: BookCreate):
    """Creates a new Book in the database."""
    book_id = bookdb.create_book(book)
    # Fixed typo: module_dump() changed to model_dump()
    return model.Book(id=book_id, **book.model_dump())

@app.get("/Book/", response_model=List[Book])
def read_books():
    """Retrieves all Books from the database."""
    return bookdb.read_books()

@app.get("/Book/{book_id}", response_model=Book)
def read_book(book_id: int):
    """Retrieves a single book by its ID."""
    book = bookdb.read_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/Book/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate):
    """Updates an existing Book in the database."""
    updated = bookdb.update_book(book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    # Return the full updated object instead of just the ID to match response_model=Book
    return model.Book(id=book_id, **book.model_dump())

@app.delete("/Book/{book_id}", response_model=dict)
def delete_book(book_id: int):
    """Deletes a Book from the database by its ID."""
    deleted = bookdb.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
