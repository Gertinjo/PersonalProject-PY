from fastapi import FastAPI, HTTPException
from typing import List
import database
import Module
from Module import student, studentCreate

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the student CRUD API"}

@app.post("/student/", response_model=dict)
def create_student(student: studentCreate):
    student_id = database.create_student(student)
    return Module.student(id=student_id, **student.model_dump())

# @app.get("/student/", response_model=dict)
# def read_student():
#     """Retrieves all Books from the database."""
#     return database.read_student()

@app.get("/student/{student_id}", response_model=dict)
def read_student(student_id: int):
    """Retrieves a single book by its ID."""
    student = database.read_student(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")
    return student

@app.put("/student/{student_id}", response_model=dict)
def update_student(student_id: int, student: studentCreate):
    """Updates an existing Book in the database."""
    updated = database.update_student(student_id, student)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    # Return the full updated object instead of just the ID to match response_model=Book
    return Module.student(id=student_id, **student.model_dump())

@app.delete("/student/{student_id}", response_model=dict)
def delete_student(student_id: int):
    """Deletes a Book from the database by its ID."""
    deleted = database.delete_student(student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="student not found")
    return {"message": "student deleted successfully"}
