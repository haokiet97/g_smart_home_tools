import asyncio
import ffmpeg
from telegram import Bot
from telegram.constants import ParseMode

# Your Telegram Bot token
BOT_TOKEN = '' # Replace with your actual bot token

# Your own user ID for Saved Messages
CHAT_ID = ''  # Replace with your actual user ID

# The HLS stream URL
HLS_URL = ''


async def start_stream():
    bot = Bot(token=BOT_TOKEN)

    # FFmpeg command to read HLS and output to a format Telegram can stream
    stream = (
        ffmpeg
        .input(HLS_URL)
        .output('pipe:', format='rawvideo', pix_fmt='yuv420p', vcodec='libx264')
        .overwrite_output()
        .run_async(pipe_stdout=True)
    )

    # Start the Telegram live stream to Saved Messages
    message = await bot.send_video(
        chat_id=CHAT_ID,
        video=stream.stdout,
        supports_streaming=True,
        caption="Live Stream in Saved Messages",
        parse_mode=ParseMode.HTML
    )

    print(f"Stream started in Saved Messages")

    # Keep the script running
    while True:
        await asyncio.sleep(3)


if __name__ == '__main__':
    asyncio.run(start_stream())
