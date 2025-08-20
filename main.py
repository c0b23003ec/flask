from flask import Flask
from threading import Thread
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests

# ===== Flask =====
app = Flask("")

@app.route("/")
def home():
    return "I am alive!"

def run():
    port = int(os.environ.get("PORT", 8080))  # ← Koyeb が渡すPORTを優先
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ===== Discord Bot =====
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Load token
load_dotenv()
TOKEN = os.environ["TOKEN"]

# GAS URL
GAS_URL = os.environ.get("GAS_URL")  # Koyebの環境変数に設定しておく

def send_to_gas(user, message):
    """DiscordのメッセージをGASに送信"""
    payload = {"user": str(user), "message": message}
    try:
        response = requests.post(GAS_URL, json=payload)
        print("GAS response:", response.text)
    except Exception as e:
        print("Failed to send to GAS:", e)

@bot.event
async def on_ready():
    print(f"ログイン完了: {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # 返信例
    if message.content == "おはよう":
        await message.channel.send("おはよう！迎え！")
    # GASにメッセージ送信
    send_to_gas(message.author.name, message.content)
    await bot.process_commands(message)

# ===== 実行 =====
keep_alive()
bot.run(TOKEN)
