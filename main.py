import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import requests
import time
from datetime import datetime

# --- SERVIDOR WEB DE PERSISTÊNCIA (RENDER 24/7) ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Matrix ULTIMATE 24/7 Ativo!")

def rodar_servidor_web():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=rodar_servidor_web, daemon=True).start()

# --- CONFIGURAÇÕES ---
TOKEN = "8626894323:AAE3MBH9csoWwiqh0hS0va1Aitzmb9r7p2o"
CHAT_ID = "@AlgoritmoMatrixDouble2026"
URL_API_BLAZE = "https://blaze.com/api/roulette_games/recent"

ultimo_id_processado = None
sinal_ativo = None
ultimo_minuto_alerta_branco = -1

def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

def obter_ultimos_resultados():
    try:
        resposta = requests.get(URL_API_BLAZE, timeout=10)
        if resposta.status_code == 200:
            dados = resposta.json()
            resultados = []
            for item in dados[:15]:
                cor = item.get("color")
                if cor == 1:
                    resultados.append("🔴")
                elif cor == 2:
                    resultados.append("🖤")
                elif cor == 0:
                    resultados.append("⚪")
            id_atual = dados[0].get("id") if dados else None
            return id_atual, resultados
    except Exception as e:
        print(f"Erro na API da Blaze: {e}")
    return None, []

enviar_mensagem("🚀 *ALGORITMO MATRIX ULTIMATE:* Robô atualizado com alta frequência de sinais e inteligência Surf + Minutos!")

while True:
    id_atual, resultados = obter_ultimos_resultados()
    
    if id_atual and id_atual != ultimo_id_processado and len(resultados) >= 10:
        ultimo_id_processado = id_atual
        
        historico_10 = " ".join(resultados[:10])
        ultima_pedra = resultados[0]
        minuto_atual = datetime.now().minute
        
        # 1. CONFERÊNCIA DE GREEN / LOSS DO SINAL ANTERIOR
        if sinal_ativo:
            cor_esperada = sinal_ativo['entrada']
            if ultima_pedra == cor_esperada or ultima_pedra == "⚪":
                enviar_mensagem(f"✅ **GREEN CONFIRMADO!** ({ultima_pedra})\n🎯 Resultado alinhado com a estratégia!")
            else:
                enviar_mensagem("❌ **LOSS** — Mantenha a gestão de banca!")
            sinal_ativo = None

        # 2. PADRÃO SURF (TENDÊNCIA: 4+ SEGUIDOS -> APOSTAR A FAVOR DA COR)
        elif resultados[:4] == ["🔴", "🔴", "🔴", "🔴"]:
            sinal_ativo = {'entrada': "🔴"}
            mensagem = f"""
🏄‍♂️ **PADRÃO SURF DETECTADO (TENDÊNCIA)** 🏄‍♂️

📊 **Pedras ao Vivo:** {historico_10}

🎯 **Entrada Principal:** VERMELHO 🔴
⚪ **Proteção:** BRANCO ⚪
⚡ **Estratégia:** Surfando a tendência (Gale 1)
"""
            enviar_mensagem(mensagem)

        elif resultados[:4] == ["🖤", "🖤", "🖤", "🖤"]:
            sinal_ativo = {'entrada': "🖤"}
            mensagem = f"""
🏄‍♂️ **PADRÃO SURF DETECTADO (TENDÊNCIA)** 🏄‍♂️

📊 **Pedras ao Vivo:** {historico_10}

🎯 **Entrada Principal:** PRETO 🖤
⚪ **Proteção:** BRANCO ⚪
⚡ **Estratégia:** Surfando a tendência (Gale 1)
"""
            enviar_mensagem(mensagem)

        # 3. GATILHO DE BRANCO POR MINUTO PAGADOR
        elif "⚪" not in resultados[:8] and minuto_atual % 5 == 0 and minuto_atual != ultimo_minuto_alerta_branco:
            ultimo_minuto_alerta_branco = minuto_atual
            mensagem = f"""
⚪ **ALERTA DE BRANCO (MINUTO PAGADOR)** ⚪

📊 **Pedras ao Vivo:** {historico_10}

⏰ **Análise:** Minuto pagador e Branco sumido há 8+ rodadas!
🎯 **Dica de Entrada:** Cobrir BRANCO ⚪ nas próximas 2 a 3 rodadas!
"""
            enviar_mensagem(mensagem)

        # 4. PADRÃO REPETIÇÃO LHO (3 Vermelhos -> Entrar Preto)
        elif resultados[:3] == ["🔴", "🔴", "🔴"]:
            sinal_ativo = {'entrada': "🖤"}
            mensagem = f"""
🤖 **SINAL CONFIRMADO - MATRIX ULTIMATE** 🤖

📊 **Pedras ao Vivo:** {historico_10}

🎯 **Entrada Principal:** PRETO 🖤
⚪ **Proteção:** BRANCO ⚪
⚡ **Estratégia:** Quebra de Sequência (Gale 1)
"""
            enviar_mensagem(mensagem)

        # 5. PADRÃO REPETIÇÃO PRETO (3 Pretos -> Entrar Vermelho)
        elif resultados[:3] == ["🖤", "🖤", "🖤"]:
            sinal_ativo = {'entrada': "🔴"}
            mensagem = f"""
🤖 **SINAL CONFIRMADO - MATRIX ULTIMATE** 🤖

📊 **Pedras ao Vivo:** {historico_10}

🎯 **Entrada Principal:** VERMELHO 🔴
⚪ **Proteção:** BRANCO ⚪
⚡ **Estratégia:** Quebra de Sequência (Gale 1)
"""
            enviar_mensagem(mensagem)

        # 6. PADRÃO XADREZ (🔴 🖤 🔴 -> Entrar Preto)
        elif resultados[:3] == ["🔴", "🖤", "🔴"]:
            sinal_ativo = {'entrada': "🖤"}
            mensagem = f"""
⚡ **PADRÃO XADREZ DETECTADO** ⚡

📊 **Pedras ao Vivo:** {historico_10}

🎯 **Entrada Principal:** PRETO 🖤
⚪ **Proteção:** BRANCO ⚪
⚡ **Estratégia:** Alternância de Cores (Gale 1)
"""
            enviar_mensagem(mensagem)

        # 7. PADRÃO XADREZ (🖤 🔴 🖤 -> Entrar Vermelho)
        elif resultados[:3] == ["🖤", "🔴", "🖤"]:
            sinal_ativo = {'entrada': "🔴"}
            mensagem = f"""
⚡ **PADRÃO XADREZ DETECTADO** ⚡

📊 **Pedras ao Vivo:** {historico_10}

🎯 **Entrada Principal:** VERMELHO 🔴
⚪ **Proteção:** BRANCO ⚪
⚡ **Estratégia:** Alternância de Cores (Gale 1)
"""
            enviar_mensagem(mensagem)

        # 8. PADRÃO DUPLO DUPLO (🖤 🖤 🔴 🔴 -> Entrar Vermelho)
        elif resultados[:4] == ["🖤", "🖤", "🔴", "🔴"]:
            sinal_ativo = {'entrada': "🔴"}
            mensagem = f"""
🔥 **PADRÃO DUPLO DUPLO DETECTADO** 🔥

📊 **Pedras ao Vivo:** {historico_10}

🎯 **Entrada Principal:** VERMELHO 🔴
⚪ **Proteção:** BRANCO ⚪
⚡ **Estratégia:** Repetição de Pares (Gale 1)
"""
            enviar_mensagem(mensagem)

        # 9. GATILHO RÁPIDO (2 Pretos ou 2 Vermelhos -> Entrada de confirmação)
        elif resultados[:2] == ["🔴", "🔴"]:
            sinal_ativo = {'entrada': "🖤"}
            mensagem = f"""
🎯 **SINAL DE ALTA FREQUÊNCIA** 🎯

📊 **Pedras ao Vivo:** {historico_10}

🎯 **Entrada Principal:** PRETO 🖤
⚪ **Proteção:** BRANCO ⚪
⚡ **Estratégia:** Reversão Curta (Gale 1)
"""
            enviar_mensagem(mensagem)

        elif resultados[:2] == ["🖤", "🖤"]:
            sinal_ativo = {'entrada': "🔴"}
            mensagem = f"""
🎯 **SINAL DE ALTA FREQUÊNCIA** 🎯

📊 **Pedras ao Vivo:** {historico_10}

🎯 **Entrada Principal:** VERMELHO 🔴
⚪ **Proteção:** BRANCO ⚪
⚡ **Estratégia:** Reversão Curta (Gale 1)
"""
            enviar_mensagem(mensagem)

    time.sleep(5)
