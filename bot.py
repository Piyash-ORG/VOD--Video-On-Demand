import os
from pyrogram import Client, filters
from pyrogram.types import Message
import subprocess

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("ott_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("👋 Send me any OTT video link to download.")

@app.on_message(filters.text & ~filters.command("start"))
async def download(client, message: Message):
    url = message.text.strip()
    msg = await message.reply("📥 Downloading...")
    file_name = "video.mp4"

    try:
        subprocess.run(f"yt-dlp -o {file_name} '{url}'", shell=True)
        await msg.edit("✅ Uploading now...")
        await client.send_document(message.chat.id, document=file_name, caption="🎬 Here's your video")
        os.remove(file_name)
    except Exception as e:
        await msg.edit(f"❌ Error: {e}")

app.run()
