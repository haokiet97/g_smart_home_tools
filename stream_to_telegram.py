import asyncio
import ffmpeg
from telegram import Bot
from telegram.constants import ParseMode
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Your Telegram Bot token
BOT_TOKEN = ''

# The group ID where you want to stream
GROUP_ID = ''  # Make sure this starts with '-'

# The HLS stream URL
HLS_URL = ''


async def start_stream():
    bot = Bot(token=BOT_TOKEN)

    logging.info("Starting FFmpeg process")
    # FFmpeg command to read HLS and output to a format Telegram can stream
    stream = (
        ffmpeg
        .input(HLS_URL)
        .output('pipe:', format='rawvideo', pix_fmt='yuv420p', vcodec='libx264')
        .overwrite_output()
        .run_async(pipe_stdout=True, pipe_stderr=True)
    )

    logging.info("FFmpeg process started")

    # Read FFmpeg stderr in a separate task to log its output
    async def log_ffmpeg_output(stream):
        while True:
            output = await stream.stderr.readline()
            if output:
                logging.info(output.decode().strip())
            else:
                break

    asyncio.create_task(log_ffmpeg_output(stream))

    logging.info("Starting Telegram live stream")
    # Start the Telegram live stream
    message = await bot.send_video(
        chat_id=GROUP_ID,
        video=stream.stdout,
        supports_streaming=True,
        caption="Live Stream",
        parse_mode=ParseMode.HTML
    )

    logging.info("Stream started in the group")

    # Keep the script running
    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(start_stream())
