import os
import subprocess
import shutil
import fnmatch
import re
import requests

def ls(path="."):
    """List directory contents."""
    try:
        items = os.listdir(path)
        return {"items": items, "path": os.path.abspath(path)}
    except Exception as e:
        return {"error": str(e)}

def cat(path):
    """Read file content."""
    try:
        with open(path, "r") as f:
            content = f.read()
        return {"content": content, "path": os.path.abspath(path)}
    except Exception as e:
        return {"error": str(e)}

def write(path, content):
    """Write content to a file."""
    try:
        with open(path, "w") as f:
            f.write(content)
        return {"success": True, "path": os.path.abspath(path)}
    except Exception as e:
        return {"error": str(e)}

def append(path, content):
    """Append content to a file."""
    try:
        with open(path, "a") as f:
            f.write(content)
        return {"success": True, "path": os.path.abspath(path)}
    except Exception as e:
        return {"error": str(e)}

def delete(path):
    """Delete a file or directory."""
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def mkdir(path):
    """Create a directory."""
    try:
        os.makedirs(path, exist_ok=True)
        return {"success": True, "path": os.path.abspath(path)}
    except Exception as e:
        return {"error": str(e)}

def move(src, dst):
    """Move a file or directory."""
    try:
        shutil.move(src, dst)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def copy(src, dst):
    """Copy a file or directory."""
    try:
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def find(pattern, path="."):
    """Find files by name pattern."""
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return {"matches": matches}

def grep(pattern, path="."):
    """Search for text in files."""
    results = []
    regex = re.compile(pattern)
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, "r", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        if regex.search(line):
                            results.append({
                                "file": file_path,
                                "line": line_num,
                                "content": line.strip()
                            })
            except Exception:
                continue
    return {"results": results}

def edit(path, old_text, new_text):
    """Replace text in a file."""
    try:
        with open(path, "r") as f:
            content = f.read()
        if old_text not in content:
            return {"error": "Target text not found", "success": False}
        new_content = content.replace(old_text, new_text)
        with open(path, "w") as f:
            f.write(new_content)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def bash(command):
    """Execute a shell command."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "code": result.returncode
        }
    except Exception as e:
        return {"error": str(e)}

def python(code):
    """Execute a Python snippet."""
    import sys
    import io
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    try:
        exec(code)
        return {"output": new_stdout.getvalue(), "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}
    finally:
        sys.stdout = old_stdout

def fetch(url, method="GET", json=None, headers=None):
    """Perform an HTTP request."""
    try:
        response = requests.request(method, url, json=json, headers=headers)
        return {
            "status": response.status_code,
            "body": response.text,
            "headers": dict(response.headers)
        }
    except Exception as e:
        return {"error": str(e)}
