import os

def generate_code_from_description(description, project_path):
    description = description.lower()
    if "web app" in description:
        app_code = """from flask import Flask
from datetime import datetime
app = Flask(__name__)
@app.route('/')
def index():
    return str(datetime.now())
if __name__ == "__main__":
    app.run(debug=True)
"""
        req_code = "flask\n"
        with open(os.path.join(project_path, "app.py"), "w") as f:
            f.write(app_code)
        with open(os.path.join(project_path, "requirements.txt"), "w") as f:
            f.write(req_code)
    else:
        # fallback: simple print app
        app_code = f'print("{description}")\n'
        with open(os.path.join(project_path, "app.py"), "w") as f:
            f.write(app_code)
        with open(os.path.join(project_path, "requirements.txt"), "w") as f:
            f.write("")
