import os
import time
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Online!")

threading.Thread(target=lambda: HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), SimpleHTTPRequestHandler).serve_forever(), daemon=True).start()

TOKEN = "8626894323:AAE3hW8csoWiqbW58va1AiZw9r7p2o"
CHAT_ID = "@AlgoritmoMatrixDouble2026"
URL_BLAZE = "https://blaze.com/api/roulette_games/recent"

def enviar_telegram(texto):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "HTML"}, timeout=5)
    except Exception as e:
        print(f"Erro Telegram: {e}")

enviar_telegram("🤖 <b>BOT TESTANDO CONEXÃO COM A BLAZE...</b>")

ultima_rodada_id = None

while True:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }
        
        response = requests.get(URL_BLAZE, headers=headers, timeout=10)
        
        if response.status_code != 200:
            enviar_telegram(f"⚠️ <b>Erro HTTP da Blaze:</b> Status {response.status_code}")
            time.sleep(10)
            continue

        dados = response.json()
        if dados and isinstance(dados, list) and len(dados) > 0:
            rodada_recente = dados[0]
            id_atual = rodada_recente.get('id')
            
            if id_atual != ultima_rodada_id:
                pedras = [item.get('color') for item in dados[:10]]
                enviar_telegram(f"✅ <b>Conexão OK!</b> Rodada detectada (ID: {id_atual}). Cores: {pedras[:3]}")
                ultima_rodada_id = id_atual
        else:
            enviar_telegram("⚠️ A API retornou dados vazios.")

    except Exception as e:
        enviar_telegram(f"❌ <b>Erro ao processar JSON/Rede:</b> {str(e)}")

    time.sleep(5)
