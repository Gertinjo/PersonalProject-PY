from pydantic import BaseModel

class studentCreate(BaseModel):
    Name: str
    Grade: str
    Teacher: str
    Class: str
class student(studentCreate):
    id: int