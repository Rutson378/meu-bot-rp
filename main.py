import os
import telebot
import google.generativeai as genai

# Suas chaves que você me passou
TELEGRAM_TOKEN = '8513801343:AAHSF5s9HIFu4jAyPaty2pg9Wl9uuoPYfbY'
GEMINI_API_KEY = 'AIzaSyC4Hsa4V5xk1WgLCBYS7jS71K5-YYBrPX8'

# Configurando o Gemini
genai.configure(api_key=GEMINI_API_KEY)
# Usando o flash que é mais rápido e grátis
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Instrução de personalidade (O "System Prompt")
# Você pode mudar esse texto abaixo para o personagem que quiser
SYSTEM_PROMPT = "Você é o Max, um rapaz gente boa, direto, usa gírias e fala 'papo reto'. Você está num roleplay com o Rutson. Não seja polido demais, seja um parça autêntico."

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # Monta o contexto para o Gemini
        full_prompt = f"{SYSTEM_PROMPT}\n\nUsuário: {message.text}\nMax:"
        
        response = model.generate_content(full_prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Erro: {e}")
        bot.reply_to(message, "Deu algum pau aqui na IA, tenta de novo.")

print("Bot rodando...")
bot.infinity_polling()
