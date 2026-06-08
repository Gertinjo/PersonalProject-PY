from fastapi import FastAPI, HTTPException
from typing import List
import database
import Module
from Module import Student, StudentCreate

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student CRUD API"}

@app.post("/Students/", response_model=Student)
def create_student(Student: StudentCreate):
    """Creates a new Book in the database."""
    Student_id = database.create_book(Student)
    # Fixed typo: module_dump() changed to model_dump()
    return Module.Student(id=Student_id, **Student.model_dump())

@app.get("/Student/", response_model=List[Student])
def read_student():
    """Retrieves all Books from the database."""
    return database.read_Student()

@app.get("/Student/{Student_id}", response_model=Student)
def read_student(student_id: int):
    """Retrieves a single book by its ID."""
    Student = database.read_book(student_id)
    if Student is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return Student

@app.put("/Student/{Student_id}", response_model=Student)
def update_student(Student_id: int, Student: StudentCreate):
    """Updates an existing Book in the database."""
    updated = database.update_book(Student_id, Student)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    # Return the full updated object instead of just the ID to match response_model=Book
    return Module.Student(id=Student_id, **Student.model_dump())

@app.delete("/Student/{Student_id}", response_model=dict)
def delete_student(Student_id: int):
    """Deletes a Book from the database by its ID."""
    deleted = database.delete_book(Student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
