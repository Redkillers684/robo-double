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
TOKEN = "8626894323:AAE1bN6o3tV5-7389"
CHAT_ID = "@AlgoritmoMatrixDouble2026"
URL_API_BLAZE = "https://blaze.com/api/roulette_games/recent"

def enviar_telegram(mensagem):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "HTML"}
        res = requests.post(url, json=payload, timeout=5)
        return res.status_code
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        return None

print("=== INICIANDO ROBÔ MATRIX ULTIMATE - VERSÃO ESTÁVEL ===")
enviar_telegram("🚀 <b>ALGORITMO MATRIX ULTIMATE ON!</b>\n\nRobô atualizado e monitorando a Blaze em tempo real!")

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
        if dados:
            pedras = [x['color'] for x in dados[:10]]
            id_atual = dados[0]['id']

            if id_atual != ultima_rodada_analisada:
                ultima_rodada_analisada = id_atual
                print(f"Últimas pedras (0=Branco, 1=Vermelho, 2=Preto): {pedras[:5]}")

                # Contador para o Radar do Branco
                rodadas_sem_branco = 0
                for p in pedras:
                    if p == 0:
                        break
                    rodadas_sem_branco += 1

                if rodadas_sem_branco >= 12:
                    msg_branco = (
                        f"🚨 <b>RADAR DO BRANCO ATIVADO!</b>\n\n"
                        f"⚪ <b>Alerta:</b> Já são {rodadas_sem_branco} rodadas seguidas sem sair Branco!\n"
                        f"🎯 <b>Sugestão:</b> Proteger no Branco nas próximas rodadas."
                    )
                    enviar_telegram(msg_branco)
                    print("Alerta do Radar do Branco enviado!")

                # Lógica de Padrões Simplificada e Eficiente
                # 1. SURF (3 da mesma cor: 1=Vermelho, 2=Preto)
                if pedras[0] == pedras[1] == pedras[2] and pedras[0] in [1, 2]:
                    cor_alvo = pedras[0]
                    nome_cor = "🔴 VERMELHO" if cor_alvo == 1 else "⚫ PRETO"
                    msg_sinal = (
                        f"🎯 <b>SINAL CONFIRMADO! (SURF)</b>\n\n"
                        f"📊 <b>Padrão:</b> 3 Cores Iguais\n"
                        f"➡️ <b>Entrada:</b> {nome_cor}\n"
                        f"⚪ <b>Proteção:</b> Branco (14x)\n"
                        f"🔄 <b>Gale:</b> Até 1 proteção"
                    )
                    enviar_telegram(msg_sinal)
                    print("Sinal de Surf enviado com sucesso!")

                # 2. XADREZ (Alternado: Vermelho, Preto, Vermelho ou inverso)
                elif pedras[0] != pedras[1] and pedras[1] != pedras[2] and all(p in [1, 2] for p in pedras[:3]):
                    cor_alvo = 1 if pedras[0] == 2 else 2
                    nome_cor = "🔴 VERMELHO" if cor_alvo == 1 else "⚫ PRETO"
                    msg_sinal = (
                        f"🎯 <b>SINAL CONFIRMADO! (XADREZ)</b>\n\n"
                        f"📊 <b>Padrão:</b> Alternância 1x1\n"
                        f"➡️ <b>Entrada:</b> {nome_cor}\n"
                        f"⚪ <b>Proteção:</b> Branco (14x)\n"
                        f"🔄 <b>Gale:</b> Até 1 proteção"
                    )
                    enviar_telegram(msg_sinal)
                    print("Sinal de Xadrez enviado com sucesso!")

    except Exception as e:
        print(f"Erro no loop principal: {e}")

    time.sleep(10)
