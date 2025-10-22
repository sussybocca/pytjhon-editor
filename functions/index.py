import os
import tempfile
from urllib.parse import parse_qs
from builder import code_generator

def handler(event, context):
    method = event.get("httpMethod", "GET")
    
    if method == "GET":
        # Serve editor page
        with open("templates/index.html") as f:
            html = f.read()
        return {"statusCode": 200, "headers": {"Content-Type": "text/html"}, "body": html}
    
    if method == "POST":
        body = parse_qs(event.get("body") or "")
        project_name = body.get("project_name", ["temp_project"])[0]
        code = body.get("code", [""])[0]
        description = body.get("description", [""])[0]

        project_path = os.path.join(tempfile.gettempdir(), project_name)
        os.makedirs(project_path, exist_ok=True)

        # Save code or generate from description
        if code:
            with open(os.path.join(project_path, "app.py"), "w") as f:
                f.write(code)
            with open(os.path.join(project_path, "requirements.txt"), "w") as f:
                f.write("")
        elif description:
            code_generator.generate_code_from_description(description, project_path)

        # Redirect to console function
        return {
            "statusCode": 302,
            "headers": {"Location": f"/.netlify/functions/console?project={project_name}"}
        }
