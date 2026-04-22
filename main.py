import os
import telebot
import google.generativeai as genai
from flask import Flask
import threading

# Chaves
TELEGRAM_TOKEN = '8513801343:AAFiPVFn50oWULkSp2388aDr_uah3Wlj6jQ'
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

app = Flask(__name__)
@app.route('/')
def health_check():
    return "Bot Online", 200

def run_flask():
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080))

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
        print(f"Erro: {e}")

if __name__ == "__main__":
    # Inicia o servidor falso em segundo plano
    threading.Thread(target=run_flask).start()
    print("Bot rodando...")
    bot.infinity_polling()
