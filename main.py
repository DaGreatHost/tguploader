import os
from flask import Flask, request
import telebot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    caption = request.form.get("caption", "")
    channel = request.form.get("channel", "")

    file_path = f"temp_{file.filename}"
    file.save(file_path)

    try:
        if file.mimetype.startswith("video"):
            bot.send_video(channel, open(file_path, "rb"), caption=caption)
        else:
            bot.send_photo(channel, open(file_path, "rb"), caption=caption)
        return "✅ Uploaded successfully!"
    except Exception as e:
        return f"❌ Failed to upload: {str(e)}"
    finally:
        os.remove(file_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
