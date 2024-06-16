import os
import logging
from telethon.sync import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotos
from dotenv import load_dotenv
from datetime import datetime, timezone

# Load environment variables
load_dotenv()

# Ensure logs directory exists
os.makedirs('telegram_image_scraper/logs', exist_ok=True)

# Set up logging
logging.basicConfig(filename='telegram_image_scraper/logs/telegram_image_scraper.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

logging.info('Starting Telegram Image Scraper for CheMed123')
# Configuration
api_id = '22547234'
api_hash = '726e49bdd7bb90526f728ef416eb9b5e'
phone = '+251960779709'



# Directory to save images
SAVE_DIR = 'telegram_images_for_lobelia4cosmetics'

# Create save directory if it doesn't exist
os.makedirs(SAVE_DIR, exist_ok=True)

# Connect to Telegram
client = TelegramClient(phone, api_id, api_hash)

# Function to download images
async def download_images(channel, start_date=None, end_date=None, max_images=None):
    image_count = 0
    async for message in client.iter_messages(channel, filter=InputMessagesFilterPhotos):
        message_date = message.date.replace(tzinfo=timezone.utc)  # Make message date timezone aware
        if (start_date and message_date < start_date) or (end_date and message_date > end_date):
            continue
        if max_images and image_count >= max_images:
            break
        # Download the photo
        await client.download_media(message.photo, file=os.path.join(SAVE_DIR, f'{message.id}.jpg'))
        image_count += 1
channel_name = 'lobelia4cosmetics'
# Start the client
with client:
    # Run the function to download images from the channel
    client.loop.run_until_complete(download_images(channel_name,start_date=datetime(2022, 6, 1, tzinfo=timezone.utc), end_date=datetime(2024, 6, 10, tzinfo=timezone.utc),max_images=75))

logging.info(f'Downloading image complete for: {channel_name}')
