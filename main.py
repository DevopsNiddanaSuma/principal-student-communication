from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from datetime import datetime
import json
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# File paths
FILE_NAME = "students.json"
PRINCIPAL_FILE = "principal.json"

# Load existing data
students = []
principals = []

if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as f:
        students = json.load(f)

if os.path.exists(PRINCIPAL_FILE):
    with open(PRINCIPAL_FILE, "r") as f:
        principals = json.load(f)

# Home route
@app.get("/")
def home():
    return {"message": "Welcome to Principal-Student Communication App!"}

# Register a student
@app.post("/register")
def register(name: str = Form(...), roll: str = Form(...)):
    for student in students:
        if student["roll"] == roll:
            return {"error": f"Student with roll number {roll} already exists."}

    student = {
        "name": name,
        "roll": roll,
        "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    students.append(student)
    with open(FILE_NAME, "w") as f:
        json.dump(students, f, indent=4)

    return {"message": "Student registered successfully!", "student": student}

# Get all students
@app.get("/students")
def get_students():
    return students

# Delete student
@app.delete("/delete/{roll}")
def delete_student(roll: str):
    global students
    students = [s for s in students if s["roll"] != roll]
    with open(FILE_NAME, "w") as f:
        json.dump(students, f, indent=4)
    return {"message": f"Deleted student with roll {roll}"}

# Update student
@app.put("/update")
def update_student(old_roll: str = Form(...), new_name: str = Form(...), new_roll: str = Form(...)):
    for student in students:
        if student["roll"] == old_roll:
            student["name"] = new_name
            student["roll"] = new_roll
            with open(FILE_NAME, "w") as f:
                json.dump(students, f, indent=4)
            return {"message": f"Updated student {old_roll}"}
    return {"error": f"Student {old_roll} not found"}

# Admin dashboard
@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard():
    with open("admin_dashboard.html", "r") as f:
        return f.read()

# Register principal
@app.post("/register_principal")
def register_principal(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    for admin in principals:
        if admin["username"] == username:
            return {"error": "Username already exists"}
    principals.append({"username": username, "email": email, "password": password})
    with open(PRINCIPAL_FILE, "w") as f:
        json.dump(principals, f, indent=4)
    return {"message": "Principal registered successfully!"}

# Login principal
@app.post("/login_principal")
def login_principal(username: str = Form(...), password: str = Form(...)):
    for admin in principals:
        if admin["username"] == username and admin["password"] == password:
            return {"success": True, "message": "Login successful!"}
    return {"success": False, "message": "Invalid credentials"}
