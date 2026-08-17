import os
import time
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Servidor web simples para o Render não dar timeout
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Matrix ULTIMATE rodando!")

def run_web_server():
    server_address = ('', 10000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()

# Configurações do Telegram
TOKEN = "8626894323:AAEJMbH9csoWWiqh0hS0va1Aitzmb9r7p2o"  # Coloque o TOKEN completo
CHAT_ID = "@AlgoritmoMatrixDouble2026"

def enviar_telegram(mensagem):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "HTML"}
        res = requests.post(url, json=payload, timeout=5)
        print(f"Status do Telegram: {res.status_code}")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

print("=== INICIANDO ROBÔ MATRIX ULTIMATE ===")
enviar_telegram("🚀 ALGORITMO MATRIX ULTIMATE ON!\nRobô ativado e monitorando a Blaze 24/7!")

ultimos_ids = []

while True:
    try:
        print("Buscando resultados da Blaze...")
        response = requests.get("https://blaze.bet/api/roulette_games/recent", timeout=5)
        if response.status_code == 200:
            dados = response.json()
            pedras = [x['color'] for x in dados[:10]]
            print(f"Últimas 10 pedras atuais: {pedras}")
            
            # Exemplo de verificação simples de padrão (2 iguais no topo)
            if len(pedras) >= 2 and pedras[0] == pedras[1] and pedras[0] in [1, 2]:
                cor_sinal = "PRETO 🖤" if pedras[0] == 1 else "VERMELHO 🔴"
                msg = f"🎰 SINAL CONFIRMADO!\n\nEntrada no: {cor_sinal}\nProteção: ⚪ Branco\n\nÚltimas pedras: {pedras}"
                print("Padrão detectado! Enviando sinal...")
                enviar_telegram(msg)
                time.sleep(30) # Pausa para aguardar a rodada fechar
        else:
            print(f"Aviso API Blaze: Status {response.status_code}")
    except Exception as e:
        print(f"Erro no loop da Blaze: {e}")
    
    time.sleep(5)
