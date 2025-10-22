import os
import tempfile
from urllib.parse import parse_qs
from builder import auto_fix

def handler(event, context):
    query = event.get("queryStringParameters") or {}
    project_name = query.get("project", "temp_project")

    project_path = os.path.join(tempfile.gettempdir(), project_name)
    output = auto_fix.auto_fix_code(project_path)

    # Simple HTML response
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Console - {project_name}</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h2>Console Output for {project_name}</h2>
        <pre>{output}</pre>
        <a href="/.netlify/functions/index">Back to Editor</a>
    </body>
    </html>
    """
    return {"statusCode": 200, "headers": {"Content-Type": "text/html"}, "body": html}
