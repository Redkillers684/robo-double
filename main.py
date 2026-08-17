import os
import time
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# --- SERVIDOR WEB PARA MANTER ONLINE ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Matrix 24/7 Ativo!")

threading.Thread(target=lambda: HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), SimpleHTTPRequestHandler).serve_forever(), daemon=True).start()

# --- CONFIGURAÇÕES ---
TOKEN = "8626894323:AAE3hW8csoWiqbW58va1AiZw9r7p2o"
CHAT_ID = "@AlgoritmoMatrixDouble2026"
URL_API_BLAZE = "https://blaze.com/api/roulette_games/recent"

def enviar_telegram(mensagem):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "HTML"}, timeout=5)
    except:
        pass

# --- LÓGICA DE SINAIS ---
ultima_rodada_analisada = None
contador_branco = 0

while True:
    try:
        # Cabeçalho adicionado para evitar bloqueio da Blaze no servidor Render
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
        res = requests.get(URL_API_BLAZE, headers=headers, timeout=5)
        
        if res.status_code == 200:
            dados = res.json()
            if dados:
                id_atual = dados[0]['id']
                
                # Só analisa se a roleta girou e gerou um novo ID
                if id_atual != ultima_rodada_analisada:
                    pedras = [x['color'] for x in dados[:10]] # 0=Branco, 1=Vermelho, 2=Preto
                    cor_atual = pedras[0]
                    
                    # Evita disparar sinal falso no exato momento que o bot liga
                    if ultima_rodada_analisada is not None:
                        
                        # 1. RADAR DO BRANCO
                        if cor_atual == 0:
                            enviar_telegram("🎉 <b>BRANCO SAIU NA BLAZE!</b>")
                            contador_branco = 0
                        else:
                            contador_branco += 1
                            if contador_branco >= 10:
                                enviar_telegram(f"🚨 <b>RADAR DO BRANCO:</b> Já passaram {contador_branco} rodadas sem sair Branco!")

                        # 2. SURF (3 cores iguais seguidas)
                        if pedras[0] == pedras[1] == pedras[2] and pedras[0] in [1, 2]:
                            cor_alvo = "🔴 VERMELHO" if pedras[0] == 1 else "⚫ PRETO"
                            enviar_telegram(f"🎯 <b>SINAL SURF!</b>\n\n➡️ <b>Entrada:</b> {cor_alvo}\n⚪ <b>Proteção:</b> Branco")

                        # 3. XADREZ (Cores alternadas: ex. V-P-V ou P-V-P)
                        elif pedras[0] != pedras[1] and pedras[1] != pedras[2] and all(p in [1, 2] for p in pedras[:3]):
                            cor_alvo = "🔴 VERMELHO" if pedras[0] == 2 else "⚫ PRETO"
                            enviar_telegram(f"🎯 <b>SINAL XADREZ!</b>\n\n➡️ <b>Entrada:</b> {cor_alvo}\n⚪ <b>Proteção:</b> Branco")

                    # Atualiza o ID para esperar a próxima rodada
                    ultima_rodada_analisada = id_atual
                    
    except Exception:
        pass
        
    time.sleep(5)
