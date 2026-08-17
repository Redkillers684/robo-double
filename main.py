import os
import time
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# --- SERVIDOR WEB PARA MANTER O RENDER ONLINE (PORTA 10000) ---
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

# --- CONFIGURAÇÕES DO TELEGRAM ---
TOKEN = "8626894323:AAEJMbH9csoWWiqh0hS0va1Aitzmb9r7p2o"
CHAT_ID = "@AlgoritmoMatrixDouble2026"
URL_API_BLAZE = "https://blaze.com/api/roulette_games/recent"

def enviar_telegram(mensagem):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "HTML"}
        res = requests.post(url, json=payload, timeout=5)
        print(f"Status Telegram: {res.status_code} - Resposta: {res.text}")
        return res.status_code
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        return None

print("=== INICIANDO ROBÔ MATRIX ULTIMATE - TESTE DE LOGS ===")
enviar_telegram("🚀 <b>ROBÔ REINICIADO E CONECTADO!</b>\n\nMonitorando a Blaze ativamente...")

ultima_rodada_analisada = None

def obter_pedras_recentes():
    try:
        res = requests.get(URL_API_BLAZE, timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Erro ao acessar API da Blaze: {e}")
    return None

while True:
    try:
        dados = obter_pedras_recentes()
        if dados and len(dados) > 0:
            pedras = [x['color'] for x in dados[:10]]
            id_atual = dados[0]['id']

            # Só analisa se mudou de rodada na Blaze
            if id_atual != ultima_rodada_analisada:
                ultima_rodada_analisada = id_atual
                print(f"Nova rodada detectada! ID: {id_atual} | Últimas cores: {pedras[:5]}")

                # 1. SURF (3 cores iguais seguidas)
                if pedras[0] == pedras[1] == pedras[2] and pedras[0] in [1, 2]:
                    cor_alvo = pedras[0]
                    nome_cor = "🔴 VERMELHO" if cor_alvo == 1 else "⚫ PRETO"
                    msg = (
                        f"🎯 <b>SINAL ENCONTRADO! (SURF)</b>\n\n"
                        f"➡️ <b>Entrada:</b> {nome_cor}\n"
                        f"⚪ <b>Proteção:</b> Branco (14x)\n"
                        f"🔄 <b>Gale:</b> Até 1 proteção"
                    )
                    enviar_telegram(msg)

                # 2. XADREZ (Alternado 1x1)
                elif pedras[0] != pedras[1] and pedras[1] != pedras[2] and all(p in [1, 2] for p in pedras[:3]):
                    cor_alvo = 1 if pedras[0] == 2 else 2
                    nome_cor = "🔴 VERMELHO" if cor_alvo == 1 else "⚫ PRETO"
                    msg = (
                        f"🎯 <b>SINAL ENCONTRADO! (XADREZ)</b>\n\n"
                        f"➡️ <b>Entrada:</b> {nome_cor}\n"
                        f"⚪ <b>Proteção:</b> Branco (14x)\n"
                        f"🔄 <b>Gale:</b> Até 1 proteção"
                    )
                    enviar_telegram(msg)

    except Exception as e:
        print(f"Erro no loop principal: {e}")

    time.sleep(5)
