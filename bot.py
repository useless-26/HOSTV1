import os
import logging
from dotenv import load_dotenv
from pyrogram import Client
import asyncio
from aiohttp import web

# Load .env file (local testing ke liye)
load_dotenv()

# --- Configuration - SAFE WAY ---
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# --- Pyrogram Client ---
class PyroHosterBot(Client):
    def __init__(self):
        super().__init__(
            "pyro_hoster_bot",
            api_id=int(API_ID),  # Yahan guarantee hai ki integer hai
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=20
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        LOGGER.info(f"✅ Bot started as {me.first_name} (@{me.username})")

# --- Health Check Server for Render ---
async def health_check(request):
    return web.Response(text="Bot is running!")

async def main():
    # Start health check server on Render's PORT
    port = int(os.environ.get("PORT", 8080))
    app_web = web.Application()
    app_web.router.add_get("/", health_check)
    
    runner = web.AppRunner(app_web)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    LOGGER.info(f"✅ Health check server running on port {port}")
    
    # Start the bot
    bot_app = PyroHosterBot()
    await bot_app.start()
    
    # Keep running
    await asyncio.Event().wait()

if __name__ == "__main__":
    # Validate environment variables
    missing = []
    if not API_ID:
        missing.append("API_ID")
    if not API_HASH:
        missing.append("API_HASH")
    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")
    
    if missing:
        LOGGER.critical(f"❌ Missing env vars: {', '.join(missing)}")
        LOGGER.critical("Set them in Render Dashboard (Environment tab)")
        exit(1)
    
    LOGGER.info("🚀 Starting PyroHosterBot...")
    asyncio.run(main())
