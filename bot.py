import os
from pyrogram import Client, filters
from mega import Mega
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Mega account login
mega = Mega()
m = mega.login()  # Use mega.login('email', 'password') if using a premium Mega account

# Pyrogram client for userbot
app = Client("mega_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(bot, message):
    await message.reply_text("Welcome! Send me a Mega.nz link to download files up to 2GB.")

@app.on_message(filters.text & filters.private)
async def download_mega(bot, message):
    link = message.text

    if "mega.nz" not in link:
        await message.reply_text("Invalid Mega.nz link. Please send a valid link.")
        return
    
    try:
        await message.reply_text("Downloading from Mega.nz...")

        # Download the file from Mega.nz
        file = m.download_url(link)
        file_path = file.name if hasattr(file, 'name') else 'file'

        # Upload the file to Telegram
        await bot.send_document(chat_id=message.chat.id, document=file_path)

        # Remove the downloaded file after upload
        os.remove(file_path)

    except Exception as e:
        await message.reply_text(f"Failed to download or upload: {e}")

if __name__ == '__main__':
    app.run()
