from flask import Flask, request
import requests
import os

app = Flask(__name__)
GEMINI_API_KEY = "YAHAN_APNI_GEMINI_API_KEY_DAALEIN"
TELEGRAM_BOT_TOKEN = "YAHAN_APNA_TELEGRAM_TOKEN_DAALEIN"
TELEGRAM_CHAT_ID = "YAHAN_APNI_CHAT_ID_DAALEIN"

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

asset = data.get("asset", "XAUUSD/BTC")
price = data.get("price", "Unknown")
condition = data.get("condition", "Setup detected")

prompt = f"""
A trading alert was triggered for {asset}.
Current Price: {price}
Condition: {condition}

As an expert trader, analyze this and format a professional trade alert:
🚨 AI TRADE SIGNAL
* Asset: {asset}
* Action: BUY / SELL
* Entry Price: {price}
* Stop Loss: [Logical stop loss]
* Target (TP): [Logical target]
* Reason: [Short technical reason]
"""

gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
headers = {"Content-Type": "application/json"}
body = {"contents": [{"parts": [{"text": prompt}]}]}

response = requests.post(gemini_url, json=body, headers=headers)
result_json = response.json()

try:
ai_text = result_json["candidates"][0]["content"]["parts"][0]["text"]
except Exception:
ai_text = "⚠️ AI analysis error occurred, but alert received."

send_telegram_message(ai_text)
return "OK", 200

if name == "main":
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
