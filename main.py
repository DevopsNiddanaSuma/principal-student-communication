from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from datetime import datetime
app = FastAPI()
templates = Jinja2Templates(directory="templates")
# Dummy credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return RedirectResponse(url="/students", status_code=302)
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid username or password"
        })

# Enable frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# File to store data
FILE_NAME = "students.json"

# Load existing data or create empty list
if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as f:
        students = json.load(f)
else:
    students = []
@app.get("/")
def home():
    return {"message":"welcome to the principal student app"}
@app.post("/register")
def register(name: str = Form(...), roll: str = Form(...)):
    # Check for duplicate roll numbers
    for student in students:
        if student["roll"] == roll:
            return {"error": f"Student with roll number {roll} already exists."}

    student = {"name": name, "roll": roll}
    students.append(student)

    # Save to file
    with open(FILE_NAME, "w") as f:
        json.dump(students, f, indent=4)

    return {"message": f"{name} registered successfully!", "total": len(students)}
   

@app.get("/students")
def get_students():
    return students
@app.delete("/delete/{roll}")
def delete_student(roll: str):
    global students
    original_count = len(students)

    # Filter out student with matching roll number
    students = [s for s in students if s["roll"] != roll]

    if len(students) < original_count:
        # Save updated list to JSON
        with open(FILE_NAME, "w") as f:
            json.dump(students, f, indent=4)
        return {"message": f"Student with roll number {roll} deleted successfully."}
    else:
        return {"error": f"No student found with roll number {roll}."}  


@app.put("/update")
def update_student(
    old_roll: str = Form(...),
    new_name: str = Form(...),
    new_roll: str = Form(...)
):
    found = False

    for student in students:
        if student["roll"] == old_roll:
            student["name"] = new_name
            student["roll"] = new_roll
            found = True
            break

    if found:
        with open(FILE_NAME, "w") as f:
            json.dump(students, f, indent=4)
        return {"message": f"Student with roll {old_roll} updated successfully."}
    else:
        return {"error": f"No student found with roll number {old_roll}."}  
