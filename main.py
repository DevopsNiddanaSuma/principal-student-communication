from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

USERS_FILE = "users.json"

# Create users.json file if not exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

@app.get("/", response_class=HTMLResponse)
def show_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": ""})

@app.post("/signup")
def signup(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)
):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    for user in users:
        if user["email"] == email:
            return templates.TemplateResponse("login.html", {"request": request, "message": "User already exists!"})
    users.append({"email": email, "password": password, "role": role})
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)
    return templates.TemplateResponse("login.html", {"request": request, "message": "Signup successful! Please login."})

@app.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)
):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    for user in users:
        if user["email"] == email and user["password"] == password and user["role"] == role:
            return templates.TemplateResponse("login.html", {"request": request, "message": f"Login successful as {role}!"})
    return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid credentials!"})
