import os
import time
import requests
import cloudscraper
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Servidor web para manter o Render ativo 24/7
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Cloudscraper Ativo!")

def iniciar_servidor():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=iniciar_servidor, daemon=True).start()

# Configurações do Telegram e API
TOKEN = "8626894323:AAE3hW8csoWiqbW58va1AiZw9r7p2o"
CHAT_ID = "@AlgoritmoMatrixDouble2026"
URL_BLAZE = "https://blaze.com/api/roulette_games/recent"

# Cria o scraper inteligente para burlar o bloqueio da Blaze
scraper = cloudscraper.create_scraper()

def enviar_telegram(texto):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        res = requests.post(url, json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "HTML"}, timeout=5)
        return res.status_code == 200
    except Exception:
        return False

enviar_telegram("🚀 <b>BOT MATRIX BLINDADO ATIVADO!</b>\n\nConexão via Cloudscraper estabelecida.")

ultima_rodada_id = None
sinal_ativo = None

while True:
    try:
        response = scraper.get(URL_BLAZE, timeout=10)
        
        if response.status_code == 200:
            dados = response.json()
            if dados and isinstance(dados, list) and len(dados) > 0:
                rodada_recente = dados[0]
                id_atual = rodada_recente.get('id')
                
                if id_atual != ultima_rodada_id:
                    pedras = [item.get('color') for item in dados[:10]]
                    cor_saiu = pedras[0]
                    
                    if sinal_ativo is not None:
                        cor_alvo = sinal_ativo['cor_alvo']
                        nome_estrategia = sinal_ativo['estrategia']
                        
                        if cor_saiu == 0:
                            enviar_telegram(f"✅ <b>GREEN NO BRANCO! ({nome_estrategia})</b> ⚪")
                        elif cor_saiu == cor_alvo:
                            enviar_telegram(f"✅ <b>GREEN! ({nome_estrategia})</b> 🎯")
                        else:
                            enviar_telegram(f"❌ <b>LOSS ({nome_estrategia})</b>")
                        
                        sinal_ativo = None

                    if ultima_rodada_id is not None and len(pedras) >= 3:
                        if pedras[0] == pedras[1] == pedras[2] and pedras[0] in [1, 2]:
                            cor_alvo = pedras[0]
                            nome_cor = "🔴 VERMELHO" if cor_alvo == 1 else "⚫ PRETO"
                            enviar_telegram(f"🎯 <b>SINAL ENCONTRADO: SURF</b>\n\n➡️ <b>Entrada:</b> {nome_cor}\n⚪ <b>Proteção:</b> Branco (14x)")
                            sinal_ativo = {'cor_alvo': cor_alvo, 'estrategia': 'SURF'}

                        elif pedras[0] != pedras[1] and pedras[1] != pedras[2] and all(p in [1, 2] for p in pedras[:3]):
                            cor_alvo = 1 if pedras[0] == 2 else 2
                            nome_cor = "🔴 VERMELHO" if cor_alvo == 1 else "⚫ PRETO"
                            enviar_telegram(f"🎯 <b>SINAL ENCONTRADO: XADREZ</b>\n\n➡️ <b>Entrada:</b> {nome_cor}\n⚪ <b>Proteção:</b> Branco (14x)")
                            sinal_ativo = {'cor_alvo': cor_alvo, 'estrategia': 'XADREZ'}

                    ultima_rodada_id = id_atual
                    
    except Exception:
        pass

    time.sleep(5)
