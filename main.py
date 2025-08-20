from flask import Flask
from threading import Thread
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# ===== Flask =====
app = Flask("")

@app.route("/")
def home():
    return "I am alive!"

def run():
    port = int(os.environ.get("PORT", 8080))  # ← 環境変数PORTを使う
    app.run(host="0.0.0.0", port=port)


def keep_alive():
    t = Thread(target=run)
    t.start()

# ===== Discord Bot =====
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
load_dotenv()
# TOKEN = os.getenv("TOKEN")
TOKEN = os.environ["TOKEN"]

@bot.event
async def on_ready():
    print(f"ログイン完了: {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "おはよう":
        await message.channel.send("おはよう！迎え！")
    await bot.process_commands(message)

# ===== 実行 =====
keep_alive()
bot.run(TOKEN)