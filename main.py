from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import json

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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
