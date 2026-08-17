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
TOKEN = "8626894323:AAE1bN6o3tV5-7389"  # Insira o Token completo se necessário
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

print("=== INICIANDO ROBÔ MATRIX ULTIMATE - COM GREEN/LOSS E RADAR BRANCO ===")
enviar_telegram("🚀 <b>ALGORITMO MATRIX ULTIMATE ON!</b>\n\nRobô ativo com monitoramento de GREEN/LOSS e Radar do Branco 24/7!")

ultima_rodada_analisada = None
limite_sem_branco = 12  # Dispara o radar após 12 rodadas sem sair branco

def obter_pedras_recentes():
    try:
        res = requests.get(URL_API_BLAZE, timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Erro ao acessar API da Blaze: {e}")
    return None

def checar_resultado_sinal(cor_alvo_code):
    """
    Monitora até 2 rodadas (Primeira entrada e Gale 1) para confirmar GREEN ou LOSS.
    cor_alvo_code: 1 para Vermelho, 2 para Preto
    """
    print("Aguardando resultado da 1ª Entrada...")
    time.sleep(30)  # Tempo para girar a rodada
    
    dados = obter_pedras_recentes()
    if not dados:
        return
    
    primeira_pedra = dados[0]['color']
    
    # 0 = Branco, 1 = Vermelho, 2 = Preto
    if primeira_pedra == 0:
        enviar_telegram("⚪ <b>GREEN NO BRANCO! (14x)</b> 🎉")
        return
    elif primeira_pedra == cor_alvo_code:
        enviar_telegram("✅ <b>GREEN DIRETO!</b> 🚀")
        return
    else:
        # Errou a 1ª entrada, faz o Gale 1
        enviar_telegram("🔄 <b>ATENÇÃO: APLICAR GALE 1!</b>")
        time.sleep(30)  # Aguarda a rodada do Gale 1
        
        dados_gale = obter_pedras_recentes()
        if not dados_gale:
            return
            
        segunda_pedra = dados_gale[0]['color']
        
        if segunda_pedra == 0:
            enviar_telegram("⚪ <b>GREEN NO BRANCO NO GALE 1! (14x)</b> 🎉")
        elif segunda_pedra == cor_alvo_code:
            enviar_telegram("✅ <b>GREEN NO GALE 1!</b> 👍")
        else:
            enviar_telegram("❌ <b>LOSS NA RODADA</b> 🔻")

while True:
    try:
        dados = obter_pedras_recentes()
        if dados:
            pedras = [x['color'] for x in dados[:15]]
            id_atual = dados[0]['id']

            if id_atual != ultima_rodada_analisada:
                ultima_rodada_analisada = id_atual
                print(f"Últimas pedras (0=Branco, 1=Vermelho, 2=Preto): {pedras[:6]}")

                # --- RADAR DO BRANCO ---
                rodadas_sem_branco = 0
                for p in pedras:
                    if p == 0:
                        break
                    rodadas_sem_branco += 1

                if rodadas_sem_branco >= limite_sem_branco:
                    msg_branco = (
                        f"🚨 <b>RADAR DO BRANCO ATIVADO!</b>\n\n"
                        f"⚪ <b>Alerta:</b> {rodadas_sem_branco} rodadas sem sair Branco!\n"
                        f"🎯 <b>Sugestão:</b> Proteger no Branco (⚪) nas próximas 3 rodadas."
                    )
                    print("Radar do Branco ativado!")
                    enviar_telegram(msg_branco)
                    time.sleep(40)
                    continue

                # --- ANÁLISE DE PADRÕES REGULARES ---
                if len(pedras) >= 4:
                    padrao = None
                    cor_entrada_str = None
                    cor_alvo_code = None

                    # 1. SURF (4 da mesma cor)
                    if pedras[0] == pedras[1] == pedras[2] == pedras[3] and pedras[0] in [1, 2]:
                        padrao = "SURF (Sequência Longa)"
                        cor_alvo_code = pedras[0]
                        cor_entrada_str = "🔴 VERMELHO" if cor_alvo_code == 1 else "⚫ PRETO"

                    # 2. XADREZ (Alternado 1x1)
                    elif pedras[0] != pedras[1] and pedras[1] != pedras[2] and pedras[2] != pedras[3] and all(p in [1, 2] for p in pedras[:4]):
                        padrao = "XADREZ (Alternado 1x1)"
                        cor_alvo_code = 1 if pedras[0] == 2 else 2
                        cor_entrada_str = "🔴 VERMELHO" if cor_alvo_code == 1 else "⚫ PRETO"

                    # 3. 2-PEDRAS (Dupla)
                    elif pedras[0] == pedras[1] and pedras[0] in [1, 2]:
                        padrao = "2-PEDRAS (Quebra de Dupla)"
                        cor_alvo_code = 2 if pedras[0] == 1 else 1
                        cor_entrada_str = "🔴 VERMELHO" if cor_alvo_code == 1 else "⚫ PRETO"

                    # Se encontrar padrão, envia sinal e monitora o resultado
                    if padrao and cor_entrada_str:
                        msg_sinal = (
                            f"🎯 <b>SINAL CONFIRMADO!</b>\n\n"
                            f"📊 <b>Padrão:</b> {padrao}\n"
                            f"➡️ <b>Entrada:</b> {cor_entrada_str}\n"
                            f"⚪ <b>Proteção:</b> Branco (14x)\n"
                            f"🔄 <b>Gale:</b> Até 1 proteção"
                        )
                        print(f"Padrão {padrao} detectado! Envia sinal...")
                        enviar_telegram(msg_sinal)
                        
                        # Chama a verificação automática de resultado
                        checar_resultado_sinal(cor_alvo_code)

    except Exception as e:
        print(f"Erro no loop principal: {e}")

    time.sleep(5)
