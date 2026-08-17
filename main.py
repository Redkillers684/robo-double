import os
import time
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Servidor web obrigatório para o Render não derrubar o bot
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Matrix Operacional!")

def iniciar_servidor():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=iniciar_servidor, daemon=True).start()

# Configurações do Telegram e API
TOKEN = "8626894323:AAE3hW8csoWiqbW58va1AiZw9r7p2o"
CHAT_ID = "@AlgoritmoMatrixDouble2026"
URL_BLAZE = "https://blaze.com/api/roulette_games/recent"

def enviar_telegram(texto):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "HTML"}, timeout=5)
    except Exception:
        pass

print("=== BOT INICIADO E MONITORANDO ===")

ultima_rodada_id = None
contador_branco = 0

while True:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }
        
        response = requests.get(URL_BLAZE, headers=headers, timeout=5)
        
        if response.status_code == 200:
            dados = response.json()
            if dados and isinstance(dados, list) and len(dados) > 0:
                rodada_recente = dados[0]
                id_atual = rodada_recente.get('id')
                
                # Executa apenas quando a roleta muda de ID (nova rodada fechada)
                if id_atual != ultima_rodada_id:
                    
                    # Se não for a primeira leitura após ligar, processa os sinais
                    if ultima_rodada_id is not None:
                        pedras = [item.get('color') for item in dados[:10]] # 0=Branco, 1=Vermelho, 2=Preto
                        cor_atual = pedras[0]
                        
                        # 1. Radar do Branco
                        if cor_atual == 0:
                            enviar_telegram("🎉 <b>SAIU BRANCO NA BLAZE! (14x)</b>")
                            contador_branco = 0
                        else:
                        
                            contador_branco += 1
                            if contador_branco >= 10:
                                enviar_telegram(f"🚨 <b>RADAR DO BRANCO:</b> Já passaram {contador_branco} rodadas seguidas sem sair Branco!")

                        # 2. Padrão Surf (3 cores iguais seguidas: Vermelho ou Preto)
                        if pedras[0] == pedras[1] == pedras[2] and pedras[0] in [1, 2]:
                            cor_nome = "🔴 VERMELHO" if pedras[0] == 1 else "⚫ PRETO"
                            enviar_telegram(
                                f"🎯 <b>SINAL ENCONTRADO: SURF!</b>\n\n"
                                f"➡️ <b>Entrada:</b> {cor_nome}\n"
                                f"⚪ <b>Proteção:</b> Branco (14x)\n"
                                f"🔄 <b>Gale:</b> Até 1 proteção"
                            )

                        # 3. Padrão Xadrez (Alternado 1x1)
                        elif pedras[0] != pedras[1] and pedras[1] != pedras[2] and all(p in [1, 2] for p in pedras[:3]):
                            cor_nome = "🔴 VERMELHO" if pedras[0] == 2 else "⚫ PRETO"
                            enviar_telegram(
                                f"🎯 <b>SINAL ENCONTRADO: XADREZ!</b>\n\n"
                                f"➡️ <b>Entrada:</b> {cor_nome}\n"
                                f"⚪ <b>Proteção:</b> Branco (14x)\n"
                                f"🔄 <b>Gale:</b> Até 1 proteção"
                            )

                    ultima_rodada_id = id_atual
                    
    except Exception:
        pass

    time.sleep(5)
