from fastapi import FastAPI, HTTPException, status
from models import Student, StudentCreate, StudentUpdate
from typing import List
from threading import Lock
import requests

app = FastAPI()

# In-memory data storage
students_db = {}
lock = Lock()

# Mock function to integrate with Ollama for student summary
def generate_summary(student: Student) -> str:
    # Placeholder for Ollama integration, replace with actual API call
    # response = requests.post("http://localhost:11434/generate_summary", json={"student": student.dict()})
    # return response.json().get("summary", "No summary available.")
    return f"Summary for {student.name}, aged {student.age}."

# CRUD Endpoints

@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate):
    with lock:
        student_id = len(students_db) + 1
        new_student = Student(id=student_id, **student.dict())
        students_db[student_id] = new_student
        return new_student

@app.get("/students", response_model=List[Student])
def get_students():
    return list(students_db.values())

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    student = students_db.get(student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student_update: StudentUpdate):
    with lock:
        student = students_db.get(student_id)
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        
        updated_data = student_update.dict(exclude_unset=True)
        updated_student = student.copy(update=updated_data)
        students_db[student_id] = updated_student
        return updated_student

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int):
    with lock:
        if student_id not in students_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        del students_db[student_id]
    return {"message": "Student deleted successfully"}

@app.get("/students/{student_id}/summary", response_model=str)
def student_summary(student_id: int):
    student = students_db.get(student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    summary = generate_summary(student)
    return summary
