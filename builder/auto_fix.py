from builder import run_project
import re
import os

def auto_fix_code(project_path, max_attempts=5):
    """Run app.py, parse errors, and attempt automatic fixes."""
    for _ in range(max_attempts):
        output = run_project.run(project_path)
        if "Traceback" not in output:
            return output  # Success!
        last_line = output.strip().splitlines()[-1]

        # SyntaxError fixing
        if "SyntaxError" in output:
            fix_syntax_error(project_path)
        # ModuleNotFoundError → add to requirements.txt
        elif "ModuleNotFoundError" in output:
            fix_missing_module(project_path, output)
        # NameError → define variable as None
        elif "NameError" in output:
            fix_name_error(project_path, output)
        else:
            break  # unknown error
    return output

def fix_syntax_error(project_path):
    path = os.path.join(project_path, "app.py")
    with open(path, "r") as f:
        code = f.read()
    # very naive fix: add colon at end if missing after def/if/for
    code = re.sub(r"(def .+)\n", r"\1:\n", code)
    code = re.sub(r"(if .+)\n", r"\1:\n", code)
    with open(path, "w") as f:
        f.write(code)

def fix_missing_module(project_path, output):
    module = re.search(r"No module named '(\w+)'", output)
    if module:
        module_name = module.group(1)
        req_path = os.path.join(project_path, "requirements.txt")
        with open(req_path, "a") as f:
            f.write(f"{module_name}\n")

def fix_name_error(project_path, output):
    var_match = re.search(r"name '(\w+)' is not defined", output)
    if var_match:
        var_name = var_match.group(1)
        path = os.path.join(project_path, "app.py")
        with open(path, "r") as f:
            code = f.read()
        # prepend variable definition at the top
        code = f"{var_name} = None\n{code}"
        with open(path, "w") as f:
            f.write(code)
