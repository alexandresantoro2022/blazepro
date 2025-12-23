from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
import os
from pathlib import Path

from blaze_bot import blaze_client

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

USERNAME = "admin"
PASSWORD = "admin123"

bot_running = False

default_config = {
    "initial_bet": 1.0,
    "stop_win": 50.0,
    "stop_loss": 20.0,
    "martingale_limit": 3,
    "email": "",
    "password": "",
    "token": ""
}

def load_config():
    try:
        with open("blaze_bot/config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return default_config

def save_config(config):
    with open("blaze_bot/config.json", "w") as f:
        json.dump(config, f, indent=4)

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == USERNAME and password == PASSWORD:
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="logged_in", value="true")
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "Usuário ou senha incorretos."})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if request.cookies.get("logged_in") != "true":
        return RedirectResponse(url="/", status_code=303)
    
    saldo = blaze_client.get_saldo()
    return templates.TemplateResponse("dashboard.html", {"request": request, "bot_running": bot_running, "saldo": saldo})

@app.get("/settings", response_class=HTMLResponse)
async def settings(request: Request):
    if request.cookies.get("logged_in") != "true":
        return RedirectResponse(url="/", status_code=303)
    config = load_config()
    return templates.TemplateResponse("settings.html", {"request": request, "config": config})

@app.post("/save_settings", response_class=HTMLResponse)
async def save_settings(request: Request, 
                        initial_bet: float = Form(...),
                        stop_win: float = Form(...),
                        stop_loss: float = Form(...),
                        martingale_limit: int = Form(...),
                        email: str = Form(...),
                        password: str = Form(...)):
    config = {
        "initial_bet": initial_bet,
        "stop_win": stop_win,
        "stop_loss": stop_loss,
        "martingale_limit": martingale_limit,
        "email": email,
        "password": password,
        "token": ""
    }
    save_config(config)
    return RedirectResponse(url="/dashboard", status_code=303)

@app.post("/start_bot")
async def start_bot(request: Request):
    global bot_running
    if request.cookies.get("logged_in") != "true":
        return RedirectResponse(url="/", status_code=303)

    if not bot_running:
        bot_running = True
        blaze_client.start()
    return RedirectResponse(url="/dashboard", status_code=303)

@app.post("/stop_bot")
async def stop_bot(request: Request):
    global bot_running
    if request.cookies.get("logged_in") != "true":
        return RedirectResponse(url="/", status_code=303)

    if bot_running:
        bot_running = False
        blaze_client.stop()
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/logs", response_class=HTMLResponse)
async def logs_page(request: Request):
    if request.cookies.get("logged_in") != "true":
        return RedirectResponse(url="/", status_code=303)
    logs = blaze_client.get_logs()
    return templates.TemplateResponse("logs.html", {"request": request, "logs": logs})

@app.get("/download/config")
async def download_config(request: Request):
    """Download the config.json file"""
    if request.cookies.get("logged_in") != "true":
        return RedirectResponse(url="/", status_code=303)
    
    config_path = "/vercel/sandbox/blaze_bot/config.json"
    if os.path.exists(config_path):
        return FileResponse(
            path=config_path,
            filename="config.json",
            media_type="application/json"
        )
    return {"error": "Config file not found"}

@app.get("/download/logs")
async def download_logs(request: Request):
    """Download logs as a text file"""
    if request.cookies.get("logged_in") != "true":
        return RedirectResponse(url="/", status_code=303)
    
    logs = blaze_client.get_logs()
    logs_path = "/vercel/sandbox/logs.txt"
    
    with open(logs_path, "w", encoding="utf-8") as f:
        for log in logs:
            f.write(log + "\n")
    
    return FileResponse(
        path=logs_path,
        filename="blaze_logs.txt",
        media_type="text/plain"
    )

@app.get("/files")
async def list_files(request: Request):
    """List all files in the sandbox directory"""
    if request.cookies.get("logged_in") != "true":
        return RedirectResponse(url="/", status_code=303)
    
    sandbox_dir = Path("/vercel/sandbox")
    files = []
    
    for item in sandbox_dir.rglob("*"):
        if item.is_file() and not str(item).startswith("/vercel/sandbox/.git"):
            relative_path = item.relative_to(sandbox_dir)
            files.append({
                "name": item.name,
                "path": str(relative_path),
                "size": item.stat().st_size,
                "download_url": f"/download/file?path={relative_path}"
            })
    
    return {"sandbox_directory": str(sandbox_dir), "files": files}

@app.get("/download/file")
async def download_file(request: Request, path: str):
    """Download any file from the sandbox directory"""
    if request.cookies.get("logged_in") != "true":
        return RedirectResponse(url="/", status_code=303)
    
    file_path = Path("/vercel/sandbox") / path
    
    # Security check: ensure the file is within the sandbox directory
    if not str(file_path.resolve()).startswith("/vercel/sandbox"):
        return {"error": "Access denied"}
    
    if file_path.exists() and file_path.is_file():
        return FileResponse(
            path=str(file_path),
            filename=file_path.name,
            media_type="application/octet-stream"
        )
    
    return {"error": "File not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
