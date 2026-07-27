import os
import time
import threading
import requests
from flask import Flask

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials missing!")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")

# Free market data checker background task
def market_scanner():
    time.sleep(5) # Bot start hone ke thodi der baad chalega
    send_telegram_message("🤖 *Free Trading Bot Active!*\n\nMonitoring BTC and XAUUSD live from public data. No TradingView required!")
    
    while True:
        try:
            # BTC live price fetch kar rahe hain Binance se (Free)
            btc_response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10)
            btc_price = float(btc_response.json()['price'])
            
            # Yahan aapki strategy / conditions check hongi aur signal aane par Telegram par message jayega
            # Filhal yeh check kar raha hai ki bot live data le raha hai
            print(f"Fetched live BTC Price: {btc_price}")
            
        except Exception as e:
            print(f"Error fetching market data: {e}")
            
        # Har 5 minute mein market check karega
        time.sleep(300)

@app.route("/")
def home():
    return "Free Trading Bot is running live for BTC and XAUUSD!"

if __name__ == "__main__":
    # Background thread start kar rahe hain taaki server bhi chale aur market bhi scan ho
    scanner_thread = threading.Thread(target=market_scanner)
    scanner_thread.daemon = True
    scanner_thread.start()
    
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
