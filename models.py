from pydantic import BaseModel, EmailStr
from typing import Optional

class Student(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr

class StudentCreate(BaseModel):
    name: str
    age: int
    email: EmailStr

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None
