from fastapi import FastAPI, HTTPException
from typing import List

import bookdb
from model import Book, BookCreate

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the books CRUD API"}


@app.post("/Book/", response_model=Book)
def create_book(book: BookCreate):
    book_id = bookdb.create_book(book)

    return Book(
        id=book_id,
        title=book.title,
        author=book.author
    )


@app.get("/Book/", response_model=List[Book])
def read_books():
    return bookdb.read_books()


@app.get("/Book/{book_id}", response_model=Book)
def read_book(book_id: int):
    book = bookdb.read_book(book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="book not found")

    return book


@app.put("/Book/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate):
    updated = bookdb.update_book(book_id, book)

    if not updated:
        raise HTTPException(status_code=404, detail="book not found")

    return Book(
        id=book_id,
        title=book.title,
        author=book.author
    )


@app.delete("/Book/{book_id}")
def delete_book(book_id: int):
    deleted = bookdb.delete_book(book_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="book not found")

    return {"message": "book deleted successfully"}