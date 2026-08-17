import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Matrix rodando 24/7!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()
import requests
import time

# Configurações do Telegram
TOKEN = "8626894323:AAEJMbH9csoWWiqh0hS0va1Aitzmb9r7p2o"
CHAT_ID = "@AlgoritmoMatrixDouble2026"

# Endpoint da Blaze
BLAZE_API_URL = "https://blaze.com/api/roulette_games/recent"

ultimo_id_processado = None

def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

def obter_ultimos_resultados():
    try:
        response = requests.get(BLAZE_API_URL, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            resultados = []
            for item in dados[:10]:
                color = item.get("color")
                if color == 1:
                    resultados.append("🔴")
                elif color == 2:
                    resultados.append("⚫")
                else:
                    resultados.append("⚪")
            return dados[0]["id"], resultados
    except Exception as e:
        print(f"Erro na API da Blaze: {e}")
    return None, []

def analisar_e_disparar(resultados):
    if len(resultados) < 5:
        return

    # Padrão 1: 4 Vermelhos seguidos -> Entrar no Preto
    if resultados[0] == "🔴" and resultados[1] == "🔴" and resultados[2] == "🔴" and resultados[3] == "🔴":
        mensagem = """
🚨 **ALGORITMO MATRIX - SINAL CONFIRMADO** 🚨

🎰 **Jogo:** Double
🎯 **Entrada:** PRETO ⚫
🛡️ **Proteção:** BRANCO ⚪
⚡ **Estratégia:** Máximo Gale 1 (G1)

⚠️ *Gerencie sua banca de forma consciente!*
"""
        enviar_mensagem(mensagem)

    # Padrão 2: 4 Pretos seguidos -> Entrar no Vermelho
    elif resultados[0] == "⚫" and resultados[1] == "⚫" and resultados[2] == "⚫" and resultados[3] == "⚫":
        mensagem = """
🚨 **ALGORITMO MATRIX - SINAL CONFIRMADO** 🚨

🎰 **Jogo:** Double
🎯 **Entrada:** VERMELHO 🔴
🛡️ **Proteção:** BRANCO ⚪
⚡ **Estratégia:** Máximo Gale 1 (G1)

⚠️ *Gerencie sua banca de forma consciente!*
"""
        enviar_mensagem(mensagem)

print("🤖 Robô Matrix ativado e monitorando em tempo real...")

while True:
    id_atual, ultimos_resultados = obter_ultimos_resultados()
    
    if id_atual and id_atual != ultimo_id_processado:
        ultimo_id_processado = id_atual
        print(f"Últimas pedras: {' '.join(ultimos_resultados)}")
        analisar_e_disparar(ultimos_resultados)
        
    time.sleep(5)
