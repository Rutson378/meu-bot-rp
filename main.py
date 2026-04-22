import os
import telebot
import google.generativeai as genai
from flask import Flask
import threading
import time

# Chaves - Use o Token NOVO que você gerou agora por último
TELEGRAM_TOKEN = '8513801343:AAE4L2-kJC5YdMPM4pcF7VDNGwvOyf3LVuU'
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot Online", 200

def run_flask():
    # Render usa a porta 10000 por padrão, o Flask precisa saber disso
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Config Max
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

SYSTEM_PROMPT = "Você é o Max, um rapaz gente boa, direto, usa gírias e fala 'papo reto'. Você está num roleplay com o Rutson."

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nUsuário: {message.text}\nMax:"
        response = model.generate_content(full_prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Erro no chat: {e}")

if __name__ == "__main__":
    # 1. Limpa qualquer webhook antigo que possa estar travando o Token
    bot.remove_webhook()
    time.sleep(1) 

    # 2. Inicia o Flask primeiro pra o Render ver que a porta abriu
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    print("Servidor Flask ativo. Iniciando Polling...")
    
    # 3. Roda o bot com skip_pending pra ele não tentar responder mensagens velhas e dar erro 409
    bot.infinity_polling(none_stop=True, skip_pending=True)
