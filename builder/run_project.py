import subprocess
import os
import sys

def run(project_path):
    venv_path = os.path.join(project_path, "venv")
    python_bin = sys.executable

    # Create virtual environment if not exists
    if not os.path.exists(venv_path):
        subprocess.run([python_bin, "-m", "venv", venv_path])

    # Install requirements
    pip_path = os.path.join(venv_path, "Scripts", "pip") if os.name == "nt" else os.path.join(venv_path, "bin", "pip")
    req_file = os.path.join(project_path, "requirements.txt")
    subprocess.run([pip_path, "install", "-r", req_file])

    # Run app.py and capture output
    python_path = os.path.join(venv_path, "Scripts", "python") if os.name == "nt" else os.path.join(venv_path, "bin", "python")
    app_file = os.path.join(project_path, "app.py")
    try:
        result = subprocess.run([python_path, app_file], capture_output=True, text=True, timeout=10)
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "Execution timed out."
