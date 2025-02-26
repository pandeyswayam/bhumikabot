import telebot
import google.generativeai as genai
import os

TELEGRAM_BOT_TOKEN = "7461440100:AAEeqnSDAWCD93D6CVkTZoQcFJy2f5qVyGI"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

GOOGLE_API_KEY = "AIzaSyA72YOKAl4_iS2mSQsuzhivPDtj7Sv2SDI"
genai.configure(api_key=GOOGLE_API_KEY)

DEFAULT_MODEL_NAME = 'gemini-pro'
model = genai.GenerativeModel(DEFAULT_MODEL_NAME)

conversation_history = {}

DEFAULT_SYSTEM_PROMPT = "You are a helpful and friendly assistant. Answer concisely and truthfully."

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Handles the /start and /help commands."""
    bot.reply_to(message, """
    hello sir im bhumi please tell me how may i help you today. 
    Just send me a message, and I'll respond.
    
    /help - Shows this message
    /reset - Clears the conversation history
    """)

@bot.message_handler(commands=['reset'])
def reset_conversation(message):
    """Handles the /reset command to clear conversation history."""
    user_id = message.from_user.id
    if user_id in conversation_history:
        del conversation_history[user_id]
    bot.reply_to(message, "Conversation history cleared.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Handles all other messages (i.e., user input for the AI)."""
    user_id = message.from_user.id
    user_message = message.text

    
    if user_id not in conversation_history:
        
        conversation_history[user_id] = model.start_chat(history=[])

    try:
        gemini_response = conversation_history[user_id].send_message(user_message)
        bot.reply_to(message, gemini_response.text)
    except Exception as e:
        print(f"Gemini API Error: {e}")
        bot.reply_to(message, "Sorry, I encountered an error while processing your request.")

if __name__ == "__main__":
    print("Starting Telegram bot...")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Error with bot polling: {e}")
    print("Bot stopped.")
