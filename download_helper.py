"""
Download Helper Script for /vercel/sandbox

This script helps you understand and access files in the /vercel/sandbox directory.

DIRECTORY INFORMATION:
- Absolute Path: /vercel/sandbox
- This is your project root directory
- All project files are stored here

HOW TO ACCESS FILES:
1. Via FastAPI Application:
   - Add download endpoints to main.py
   - Access files through HTTP endpoints
   
2. Via File System (if you have shell access):
   - cd /vercel/sandbox
   - ls -la (to list all files)
   - cat filename (to view file contents)
   
3. Via Python Scripts:
   - Use os.path.join('/vercel/sandbox', 'filename')
   - Use pathlib: Path('/vercel/sandbox') / 'filename'

EXAMPLE: Adding Download Functionality to Your FastAPI App
"""

import os
from pathlib import Path

# Get the sandbox directory
SANDBOX_DIR = Path("/vercel/sandbox")

def get_sandbox_path():
    """Returns the absolute path to the sandbox directory"""
    return str(SANDBOX_DIR.absolute())

def list_sandbox_files():
    """Lists all files in the sandbox directory"""
    files = []
    for item in SANDBOX_DIR.rglob("*"):
        if item.is_file():
            relative_path = item.relative_to(SANDBOX_DIR)
            files.append({
                "name": item.name,
                "path": str(relative_path),
                "absolute_path": str(item.absolute()),
                "size": item.stat().st_size
            })
    return files

def get_file_path(filename):
    """Returns the absolute path for a file in the sandbox"""
    return str(SANDBOX_DIR / filename)

if __name__ == "__main__":
    print(f"Sandbox Directory: {get_sandbox_path()}")
    print(f"\nCurrent Working Directory: {os.getcwd()}")
    print(f"\nFiles in sandbox:")
    for file_info in list_sandbox_files():
        print(f"  - {file_info['path']} ({file_info['size']} bytes)")
