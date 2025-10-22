from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import shutil

from builder import run_project, auto_fix, code_generator

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

PROJECTS_DIR = "projects"
os.makedirs(PROJECTS_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/create_project")
async def create_project(
    project_name: str = Form(...),
    description: str = Form(""),
    code: str = Form(""),
    app_file: UploadFile = Form(None),
    req_file: UploadFile = Form(None)
):
    project_path = os.path.join(PROJECTS_DIR, project_name)
    os.makedirs(project_path, exist_ok=True)

    # 1️⃣ Upload files
    if app_file and req_file:
        with open(os.path.join(project_path, "app.py"), "wb") as f:
            f.write(await app_file.read())
        with open(os.path.join(project_path, "requirements.txt"), "wb") as f:
            f.write(await req_file.read())
    
    # 2️⃣ Code from editor
    elif code:
        with open(os.path.join(project_path, "app.py"), "w") as f:
            f.write(code)
        # default empty requirements
        with open(os.path.join(project_path, "requirements.txt"), "w") as f:
            f.write("")

    # 3️⃣ Generate from description
    elif description:
        code_generator.generate_code_from_description(description, project_path)

    return RedirectResponse(url=f"/console?project={project_name}", status_code=303)

@app.get("/console", response_class=HTMLResponse)
async def console(request: Request, project: str):
    return templates.TemplateResponse("console.html", {"request": request, "project": project})

@app.post("/run")
async def run(project: str = Form(...)):
    project_path = os.path.join(PROJECTS_DIR, project)
    output = auto_fix.auto_fix_code(project_path)
    return {"output": output}
