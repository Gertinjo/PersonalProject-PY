from pydantic import BaseModel

class StudentCreate(BaseModel):
    Name: str
    Grade: str
    Teacher: str
    Class: str
class Student(StudentCreate):
    id: int