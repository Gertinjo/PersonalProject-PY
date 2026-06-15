from fastapi import FastAPI, HTTPException
import database
import Module
from Module import student, studentCreate, attendance, attendanceCreate

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the student CRUD API"}


# ── Student ─────────────────────────────────────────────────────────

@app.post("/student/", response_model=dict)
def create_student(student_data: studentCreate):
    student_id = database.create_student(student_data)
    return Module.student(id=student_id, **student_data.model_dump()).model_dump()


@app.get("/students/", response_model=list)
def read_students():
    return [s.model_dump() for s in database.read_students()]


@app.get("/student/{student_id}", response_model=dict)
def read_student(student_id: int):
    s = database.read_student(student_id)
    if s is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return s.model_dump()


@app.put("/student/{student_id}", response_model=dict)
def update_student(student_id: int, student_data: studentCreate):
    updated = database.update_student(student_id, student_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return Module.student(id=student_id, **student_data.model_dump()).model_dump()


@app.delete("/student/{student_id}", response_model=dict)
def delete_student(student_id: int):
    deleted = database.delete_student(student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}


# ── Attendance ──────────────────────────────────────────────────────

@app.post("/attendance/", response_model=dict)
def create_attendance(data: attendanceCreate):
    att_id = database.create_attendance(data)
    return Module.attendance(id=att_id, **data.model_dump()).model_dump()


@app.get("/attendances/", response_model=list)
def read_attendances():
    return [a.model_dump() for a in database.read_attendances()]


@app.get("/attendance/{attendance_id}", response_model=dict)
def read_attendance(attendance_id: int):
    a = database.read_attendance(attendance_id)
    if a is None:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return a.model_dump()


@app.put("/attendance/{attendance_id}", response_model=dict)
def update_attendance(attendance_id: int, data: attendanceCreate):
    updated = database.update_attendance(attendance_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return Module.attendance(id=attendance_id, **data.model_dump()).model_dump()


@app.delete("/attendance/{attendance_id}", response_model=dict)
def delete_attendance(attendance_id: int):
    deleted = database.delete_attendance(attendance_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return {"message": "Attendance record deleted successfully"}
