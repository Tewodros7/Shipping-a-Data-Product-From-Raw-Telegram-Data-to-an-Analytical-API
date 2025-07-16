# --- Environment and dependencies ---
from telethon.sync import TelegramClient
from telethon.errors import FloodWaitError, RPCError
from dotenv import load_dotenv
import os
import json
import logging
import asyncio
from datetime import datetime, timedelta
import aiofiles
import pytz

# Load variables from .env file
load_dotenv()

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
phone = os.getenv("TELEGRAM_PHONE")  # Optional: for first-time login

# Logging configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handlers for logging to file and console
if not os.path.exists('../logs'):
    os.makedirs('../logs')

# Create file and console handlers
file_handler = logging.FileHandler('../logs/scrape.log')
console_handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.handlers = []
logger.addHandler(file_handler)
logger.addHandler(console_handler)

DATA_LAKE_PATH = "../data/raw/telegram_messages"
CHANNELS = ["chemed123", "lobelia4cosmetics", "tikvahpharma"]

# Scraping date range (past 7 days)
utc = pytz.UTC
start_date = datetime.now(utc)

logger.info(f"Scraping window STARTED AT: {start_date} UTC")

async def scrape_channel(client, channel, limit=500):
    try:
        logger.info(f"Scraping from beginning for channel: {channel}")
        os.makedirs(DATA_LAKE_PATH, exist_ok=True)
        entity = await client.get_entity(channel)

        channel_path = os.path.join(DATA_LAKE_PATH, channel)
        os.makedirs(channel_path, exist_ok=True)

        count = 0

        async for message in client.iter_messages(entity, limit=limit):
            date_str = message.date.strftime("%Y-%m-%d")
            file_path = os.path.join(channel_path, f"{date_str}.json")

            message_data = {
                "message_id": message.id,
                "date": message.date.isoformat(),
                "text": message.text,
                "has_media": bool(message.media),
                "media_type": None,
                "media_path": None
            }

            if message.photo:
                media_path = os.path.join(channel_path, "images", f"{message.id}.jpg")
                os.makedirs(os.path.dirname(media_path), exist_ok=True)
                try:
                    await client.download_media(message, media_path)
                    message_data["media_type"] = "photo"
                    message_data["media_path"] = media_path
                    logger.info(f"Downloaded image for message {message.id}")
                except Exception as e:
                    logger.warning(f"X Failed to download image {message.id}: {str(e)}")

            async with aiofiles.open(file_path, "a", encoding="utf-8") as f:
                await f.write(json.dumps(message_data) + "\n")

            count += 1
            if count >= limit:
                logger.info(f"----->Reached message limit of {limit} for {channel}")
                break

            await asyncio.sleep(0.5)

        logger.info(f"=>> Finished scraping {count} messages from {channel}")

    except FloodWaitError as e:
        logger.warning(f"Rate limit: waiting {e.seconds} seconds for {channel}")
        await asyncio.sleep(e.seconds)
    except RPCError as e:
        logger.error(f"Telegram API error for {channel}: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error for {channel}: {str(e)}")

async def run_scraping():
    async with TelegramClient('session', api_id, api_hash) as client:
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            code = input("Enter the code you received: ")
            await client.sign_in(phone, code)

        for channel in CHANNELS:
            await scrape_channel(client, channel)
            logger.info(f"Sleeping 30 seconds before next channel...")
            await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(run_scraping())
    logger.info("Scraping completed.")
