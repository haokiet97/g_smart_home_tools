import asyncio
from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TimedOut
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Your Telegram Bot token
BOT_TOKEN = ''

# The group ID where you want to upload the video
GROUP_ID = ''  # Make sure this starts with '-' for groups

# Path to your video file
VIDEO_PATH = ''


async def upload_video():
    bot = Bot(token=BOT_TOKEN)

    logging.info("Starting video upload...")

    try:
        # Open the video file
        with open(VIDEO_PATH, 'rb') as video_file:
            # Upload the video
            message = await bot.send_video(
                chat_id=GROUP_ID,
                video=video_file,
                caption="Your video caption here",
                parse_mode=ParseMode.HTML,
                supports_streaming=True
            )
        logging.info(f"Video uploaded successfully. Message ID: {message.message_id}")
    except TimedOut:
        logging.error("Timed out while uploading the video. Please try again later.")


if __name__ == '__main__':
    asyncio.run(upload_video())
