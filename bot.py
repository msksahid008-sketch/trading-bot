from flask import Flask, request
import os
import requests

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }
    requests.post(url, json=payload)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return "No data", 400
    
    # Signal ka data nikalna
    asset = data.get("asset", "Unknown Asset")
    action = data.get("action", "Unknown Action")
    price = data.get("price", "Unknown Price")
    
    # Telegram ke liye message format karna
    message = f"🚨 *New Trading Signal* 🚨\n\n*Asset:* {asset}\n*Action:* {action}\n*Price:* {price}"
    
    # Message bhejna
    send_telegram_message(message)
    
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
