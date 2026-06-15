from fastapi import FastAPI, HTTPException
import database
import Module
from Module import student, studentCreate

router = FastAPI()

@router.post("/student/", response_model=dict)
def create_student(student_data: studentCreate):
    student_id = database.create_student(student_data)
    return Module.student(id=student_id, **student_data.model_dump()).model_dump()


@router.get("/students/", response_model=list)
def read_students():
    return [s.model_dump() for s in database.read_students()]


@router.get("/student/{student_id}", response_model=dict)
def read_student(student_id: int):
    s = database.read_student(student_id)
    if s is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return s.model_dump()


@router.put("/student/{student_id}", response_model=dict)
def update_student(student_id: int, student_data: studentCreate):
    updated = database.update_student(student_id, student_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return Module.student(id=student_id, **student_data.model_dump()).model_dump()


@router.delete("/student/{student_id}", response_model=dict)
def delete_student(student_id: int):
    deleted = database.delete_student(student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}