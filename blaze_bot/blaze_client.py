import time
import threading
import requests
import json

bot_active = False
thread = None
logs = []
saldo_simulado = 1000

def load_config():
    with open("blaze_bot/config.json", "r") as f:
        return json.load(f)

def salvar_token(token):
    config = load_config()
    config["token"] = token
    with open("blaze_bot/config.json", "w") as f:
        json.dump(config, f, indent=4)

def login_blaze(email, password):
    url = "https://blaze-4.com/api/auth/email/login"
    payload = {
        "email": email,
        "password": password
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            if token:
                salvar_token(token)
                logs.append("[BOT] ✅ Login realizado e token salvo!")
                return token
    except Exception as e:
        logs.append(f"[BOT] ❌ Erro ao logar: {e}")
    return None

def get_last_results():
    try:
        response = requests.get('https://blaze-4.com/api/roulette_games/recent')
        if response.status_code == 200:
            results = response.json()
            return [r['color'] for r in results[:5]]
    except Exception as e:
        logs.append(f"Erro ao obter resultados: {e}")
    return None

def decide_color(results):
    reds = results.count(1)
    blacks = results.count(2)
    if reds > blacks:
        return 2
    else:
        return 1

def fazer_aposta(token, valor, cor):
    url = "https://blaze-4.com/api/roulette_bets"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "amount": valor,
        "currency_type": "BRL",
        "color": cor
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            logs.append(f"[BOT] 🤑 Aposta enviada: R${valor} na cor {cor}")
            return True
        else:
            logs.append(f"[BOT] ⚠️ Erro ao apostar: {response.text}")
            return False
    except Exception as e:
        logs.append(f"[BOT] ❌ Erro ao apostar: {str(e)}")
        return False

def run_bot():
    global bot_active, saldo_simulado

    config = load_config()

    email = config.get("email")
    password = config.get("password")

    token = login_blaze(email, password)
    if not token:
        logs.append("[BOT] ❌ Não foi possível logar. Parando bot.")
        return

    aposta_atual = config["initial_bet"]
    stop_win = config["stop_win"]
    stop_loss = config["stop_loss"]
    martingale_limit = config["martingale_limit"]

    logs.append("[BOT] 🔥 Bot BlazePro Iniciado!")

    while bot_active:
        resultados = get_last_results()
        
        if not resultados:
            time.sleep(5)
            continue

        cor_apostar = decide_color(resultados)
        cor_nome = "Vermelho" if cor_apostar == 1 else "Preto"
        logs.append(f"[BOT] 🎯 Apostando na cor: {cor_nome}")

        aposta_realizada = fazer_aposta(token, aposta_atual, cor_apostar)
        if not aposta_realizada:
            logs.append("[BOT] ❌ Falha na aposta! Parando o bot por segurança.")
            bot_active = False
            break

        time.sleep(10)

def start():
    global bot_active, thread
    if not bot_active:
        bot_active = True
        thread = threading.Thread(target=run_bot)
        thread.start()

def stop():
    global bot_active
    bot_active = False

def get_logs():
    return logs[-30:]

def get_saldo():
    global saldo_simulado
    return saldo_simulado
