from pydantic import BaseModel

class studentCreate(BaseModel):
    name: str
    grade: str
    teacher: str
    subject: str

class student(studentCreate):
    id: int

class attendanceCreate(BaseModel):
    student_id: int
    present: bool

class attendance(attendanceCreate):
    id: int
