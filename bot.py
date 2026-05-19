import os
import logging
from aiohttp import web
from pyrogram import Client

# Environment variables
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Logging
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# Bot
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message()
async def reply(client, message):
    await message.reply("✅ Bot is running on Render!")

# Health check for Render
async def health_check(request):
    return web.Response(text="Bot is alive!")

async def start_bot():
    # Start web server for health checks
    web_app = web.Application()
    web_app.router.add_get("/", health_check)
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 10000)))
    await site.start()
    LOGGER.info("✅ Health check server started")
    
    # Start bot
    await app.start()
    LOGGER.info("✅ Bot started successfully!")
    
    # Keep running
    await asyncio.Event().wait()

if __name__ == "__main__":
    import asyncio
    
    # Check variables
    if not all([API_ID, API_HASH, BOT_TOKEN]):
        LOGGER.error("❌ Missing environment variables!")
        LOGGER.info("Set API_ID, API_HASH, BOT_TOKEN in Render Dashboard")
        exit(1)
    
    LOGGER.info("🚀 Starting bot...")
    asyncio.run(start_bot())
