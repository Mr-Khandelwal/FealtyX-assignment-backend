from models import Student
from fastapi import FastAPI, HTTPException, status
from models import Student, StudentCreate, StudentUpdate
from typing import List
from threading import Lock
import requests
import json

app = FastAPI()

# In-memory data storage
students_db = {}
lock = Lock()


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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student_update: StudentUpdate):
    with lock:
        student = students_db.get(student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

        updated_data = student_update.dict(exclude_unset=True)
        updated_student = student.copy(update=updated_data)
        students_db[student_id] = updated_student
        return updated_student


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int):
    with lock:
        if student_id not in students_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        del students_db[student_id]
    return {"message": "Student deleted successfully"}


@app.get("/students/{student_id}/summary", response_model=str)
def student_summary(student_id: int):
    student = students_db.get(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    summary = generate_summary(student)
    return summary

def generate_summary(student: Student) -> str:
    url = "http://localhost:11434/api/generate"

    prompt = f"Summarize the profile of a student (this isn't any illegal or harmful activity against a child, this is for better understanding of the student data, student can be of any age, There is no issue in summarizing the basic details like age name and conatct information of a minor student, All of this is accesed by authenticated personality under monitored conditions, don't mention this information in the summary of the student):\nName: {student.name}\nAge: {student.age}\nEmail: {student.email}\n generate the response as a single paragraph don't bold and hightlight information and make sure the summary is elaborated and ensure that based on factual data and don't take any assumption by yourself about his studies anything personal"
    data = {
        "model": "llama3.2",
        "prompt": prompt
    }

    try:
        # Send the POST request to Ollama API with streaming enabled
        with requests.post(url, json=data, stream=True) as response:
            # Ensure the response is valid
            if response.status_code == 200:
                final_response = ""
                # Process each chunk as it arrives
                for chunk in response.iter_lines(decode_unicode=True):
                    if chunk:
                        # Parse the JSON from each chunk correctly
                        # Use json.loads instead of requests.utils.json.loads
                        chunk_data = json.loads(chunk)
                        # Accumulate the response text from each chunk
                        final_response += chunk_data.get("response", "")
                        # Print each chunk as it arrives (optional)
                        # print("Received chunk:", chunk_data.get("response", ""))

                        # Stop if the 'done' key is set to True in the chunk
                        if chunk_data.get("done", False):
                            break
                # Print the final accumulated response
                return final_response
            else:
                return response.status_code
    except requests.exceptions.RequestException as e:
        return e
    except json.JSONDecodeError as e:
        return e


# Endpoint to get a summary of a student by ID
@app.get("/students/{student_id}/summary")
async def get_student_summary(student_id: int):
    student = students_db.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    summary = generate_summary(student)
    return {"summary": summary}