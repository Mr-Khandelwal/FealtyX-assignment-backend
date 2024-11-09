# FealtyX Student Management API with AI Summary Generation

This project is a backend application built with FastAPI that provides REST API endpoints to manage student data. Each student has attributes like ID, name, age, and email. Additionally, it uses the Ollama API to generate AI-driven summaries for student profiles.

## Features

- **CRUD Operations**: Perform Create, Read, Update, and Delete actions on student records.
- **AI Summary Generation**: Integrated with the Ollama language model to provide personalized summaries for each student.
- **Concurrency Handling**: Uses threading locks to handle concurrent data updates safely.
- **In-Memory Data Storage**: Data is stored in memory (using a dictionary) for simplicity.

## Project Structure

- `main.py`: Core FastAPI application with all endpoints.
- `models.py`: Data models for Student CRUD and validation.
- `requirements.txt`: Project dependencies.

## Endpoints

| Endpoint                     | Method | Description                               |
|------------------------------|--------|-------------------------------------------|
| `/students`                  | POST   | Create a new student                      |
| `/students`                  | GET    | Retrieve all students                     |
| `/students/{id}`             | GET    | Retrieve a student by ID                  |
| `/students/{id}`             | PUT    | Update a student's information by ID      |
| `/students/{id}`             | DELETE | Delete a student by ID                    |
| `/students/{id}/summary`     | GET    | Generate a summary for a student by ID    |

## Getting Started

### Prerequisites

- Python 3.8+
- FastAPI
- Requests library
- Ollama installed on localhost with `llama3.2` model

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/username/fealtyx-student-management.git
    cd fealtyx-student-management
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the FastAPI server**:
    ```bash
    uvicorn main:app --reload
    ```

### Ollama Setup

1. **Install Ollama** by following the instructions in their [Quickstart Guide](https://github.com/ollama/ollama/blob/main/README.md#quickstart).
2. **Install the llama3.2 model** in Ollama:
    ```bash
    ollama install llama3.2
    ```
3. **Configure Ollama API** to be available on `localhost:11434`.

### Usage

You can use tools like `curl`, [Postman](https://www.postman.com/), or FastAPI's Swagger UI at `http://localhost:8000/docs` to interact with the API.

**Example Requests:**

- **Create a Student**:
    ```bash
    curl -X POST http://localhost:8000/students -H "Content-Type: application/json" -d '{"name": "John Doe", "age": 20, "email": "john@example.com"}'
    ```

- **Get Student Summary**:
    ```bash
    curl http://localhost:8000/students/1/summary
    ```
