import os
import time
import requests
import ccxt
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") 

exchange = ccxt.binance()

@app.route("/")
def home():
    return "Trading Bot with Direct API is live!"

@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "").strip()
        
        if text == "/start":
            send_message(chat_id, "Hello! Bot is active. Type /price to check current Bitcoin price.")
        elif text == "/price":
            
            try:
                ticker = exchange.fetch_ticker('BTC/USDT')
                price = ticker['last']
                send_message(chat_id, f"Current BTC/USDT Price: ${price}")
            except Exception as e:
                send_message(chat_id, f"Error fetching price: {str(e)}")
        else:
            send_message(chat_id, f"Aapne kaha: {text}")
            
    return "OK", 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
