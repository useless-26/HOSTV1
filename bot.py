import os
import asyncio
import uvloop
from pyrogram import Client
from aiohttp import web

# Install uvloop for better performance
uvloop.install()

# Environment variables
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Create bot
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message()
async def handle_message(client, message):
    await message.reply("✅ Bot is running on Render!")

async def main():
    # Setup web server for health checks
    web_app = web.Application()
    
    async def health_check(request):
        return web.Response(text="Bot is alive")
    
    web_app.router.add_get("/", health_check)
    
    # Get port from environment
    port = int(os.environ.get("PORT", 10000))
    
    # Start web server
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    print(f"✅ Web server started on port {port}")
    print("✅ Bot is starting...")
    
    # Start bot
    await bot.start()
    print("✅ Bot started successfully!")
    
    # Keep everything running
    await asyncio.Event().wait()

if __name__ == "__main__":
    if not all([API_ID, API_HASH, BOT_TOKEN]):
        print("❌ Missing environment variables!")
        print("Set API_ID, API_HASH, BOT_TOKEN in Render Dashboard")
        exit(1)
    
    # Run with proper event loop
    asyncio.run(main())
