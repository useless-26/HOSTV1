import os
import logging
from dotenv import load_dotenv
from pyrogram import Client

# Load environment variables from .env file
load_dotenv()

# --- Configuration (Fixed) ---
API_ID = int(os.getenv("API_ID", "30298077"))  # ✅ Correct way
API_HASH = os.getenv("API_HASH", "124bc97f6e3bdd28a75e7115f376201f")  # ✅ Fixed
BOT_TOKEN = os.getenv("BOT_TOKEN", "8625405642:AAFZqw9qe5dz4WAm59CTkvh6gFthr1s-0d8")  # ✅ Fixed

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

# --- Pyrogram Client ---
class PyroHosterBot(Client):
    def __init__(self):
        super().__init__(
            "pyro_hoster_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=20,  # Number of concurrent workers
            plugins=dict(root="modules")  # Tells pyrogram to load plugins from 'modules' folder
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        LOGGER.info(f"✅ Bot started as {me.first_name} (@{me.username})")
        
    async def stop(self, *args):
        await super().stop()
        LOGGER.info("🛑 Bot stopped.")

if __name__ == "__main__":
    # Check if all required variables are set
    missing_vars = []
    if not API_ID:
        missing_vars.append("API_ID")
    if not API_HASH:
        missing_vars.append("API_HASH")
    if not BOT_TOKEN:
        missing_vars.append("BOT_TOKEN")
    
    if missing_vars:
        LOGGER.critical(f"❌ CRITICAL: Missing environment variables: {', '.join(missing_vars)}")
        LOGGER.info("💡 Please set them in Render Dashboard or create .env file")
        exit(1)
    
    LOGGER.info("🚀 Starting PyroHosterBot...")
    app = PyroHosterBot()
    app.run()
