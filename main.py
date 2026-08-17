import os
import time
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# --- SERVIDOR WEB (RENDER) ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Matrix ULTIMATE 24/7 Ativo!")

def rodar_servidor_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=rodar_servidor_web, daemon=True).start()

# --- CONFIGURAÇÕES ---
TOKEN = "8626894323:AAE3hW8csoWiqbW58va1AiZw9r7p2o"
CHAT_ID = "@AlgoritmoMatrixDouble2026"
URL_API_BLAZE = "https://blaze.com/api/roulette_games/recent"

def enviar_telegram(mensagem):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "HTML"}
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Erro ao enviar: {e}")

print("=== INICIANDO ROBÔ MATRIX C/ RADAR DO BRANCO ===")
ultima_rodada_analisada = None
contador_branco = 0  # Quantas rodadas sem sair Branco

while True:
    try:
        res = requests.get(URL_API_BLAZE, timeout=5)
        if res.status_code == 200:
            dados = res.json()
            if dados and len(dados) > 0:
                id_atual = dados[0]['id']
                cor_atual = dados[0]['color'] # 0=Branco, 1=Vermelho, 2=Preto

                if id_atual != ultima_rodada_analisada:
                    ultima_rodada_analisada = id_atual
                    
                    # Lógica do Radar do Branco
                    if cor_atual == 0:
                        enviar_telegram("🎉 <b>BRANCO SAIU! (14x)</b>")
                        contador_branco = 0
                    else:
                        contador_branco += 1
                        if contador_branco == 10:
                            enviar_telegram("🚨 <b>RADAR DO BRANCO:</b> O Branco está atrasado há 10 rodadas. Fique atento!")
                    
                    # Lógica de Sinais (Surf/Xadrez)
                    pedras = [x['color'] for x in dados[:10]]
                    
                    # 1. SURF
                    if pedras[0] == pedras[1] == pedras[2] and pedras[0] in [1, 2]:
                        nome = "🔴 VERMELHO" if pedras[0] == 1 else "⚫ PRETO"
                        enviar_telegram(f"🎯 <b>SINAL (SURF):</b> {nome}\n⚪ <b>Proteção:</b> Branco")

                    # 2. XADREZ
                    elif pedras[0] != pedras[1] and pedras[1] != pedras[2] and all(p in [1, 2] for p in pedras[:3]):
                        nome = "🔴 VERMELHO" if pedras[0] == 1 else "⚫ PRETO"
                        enviar_telegram(f"🎯 <b>SINAL (XADREZ):</b> {nome}\n⚪ <b>Proteção:</b> Branco")

    except Exception as e:
        print(f"Erro: {e}")

    time.sleep(5)
