import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 8080))

URL = f"https://api.telegram.org/bot{TOKEN}"
app = Flask(__name__)

def send_message(chat_id, text):
    requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": text})

@app.route("/", methods=["GET"])
def home():
    return "✅ tgcupadmin_bot is alive"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("🔔 UPDATE:", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "Привет! Это tgcupadmin_bot. Всё работает через Flask 🚀")
        else:
            send_message(chat_id, f"Ты написал: {text}")

    return {"ok": True}

if __name__ == "__main__":
    print("📡 Регистрируем вебхук...")
    r = requests.get(f"{URL}/setWebhook?url={WEBHOOK_URL}")
    print("🔗 Telegram ответил:", r.json())
    print(f"✅ Бот запущен на {WEBHOOK_URL} | PORT: {PORT}")
    app.run(host="0.0.0.0", port=PORT)
