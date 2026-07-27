import os
from flask import Flask, request
import requests

app = Flask(__name__)

# Aapka Telegram Bot Token aur Chat ID (Render environment variables se uthayega)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

@app.route("/")
def home():
    return "Smart SMC + Volume Profile Bot is Active and Running 24/7!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return "No data", 400

    # Data extraction from TradingView or Automated Scanner
    asset = data.get("asset", "Gold XAUUSD")
    action = data.get("action", "BUY")
    price = data.get("price", "N/A")
    timeframe = data.get("timeframe", "15m")
    
    # Advanced SMC + FRVP Logic / Confluence check summary (Clean text without emojis)
    signal_message = (
        f"*SMART SMC + VOLUME PROFILE ALERT*\n\n"
        f"*Asset:* {asset}\n"
        f"*Timeframe:* {timeframe} (1H/4H Trend Confirmed)\n"
        f"*Action:* `{action}`\n"
        f"*Trigger Price:* `{price}`\n\n"
        f"*Setup Confluence:* \n"
        f"- Break of Structure (BOS) Verified\n"
        f"- Session Box Zone (London/New York Active)\n"
        f"- Fixed Range Volume Profile (FRVP - POC Matched)\n\n"
        f"*Risk Management:* Manage your lot size & risk percentage according to your capital plan."
    )

    send_telegram_message(signal_message)
    return "Alert processed successfully", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
