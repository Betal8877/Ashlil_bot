import os, asyncio
from pyrogram import Client, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from moviepy.editor import VideoFileClip
from PIL import Image

API_ID = 26998965
API_HASH = "9019a06311ab5c8e0f42edfd4586be7a"
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@AshlilLinks")
VIDEO_LIFETIME = 20 * 60

app = Client("ashlil_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
scheduler = AsyncIOScheduler()
scheduler.start()

def create_thumb(path):
    clip = VideoFileClip(path)
    frame = clip.get_frame(min(clip.duration/2, 5))
    img = Image.fromarray(frame)
    thumb = path + ".jpg"
    img.save(thumb)
    return thumb

@app.on_message(filters.channel & filters.chat(CHANNEL_USERNAME) & filters.video)
async def handler(_, msg):
    file = await msg.download()
    thumb = create_thumb(file)
    sent = await msg.reply_photo(
        photo=thumb,
        caption=f"🎬 New video! ▶️ t.me/{app.me.username}?start={msg.video.file_id}\n⏳ Deletes in 20 min"
    )
    scheduler.add_job(lambda: asyncio.run_coroutine_threadsafe(
        app.delete_messages(sent.chat.id, sent.id), app.loop),
        'date', run_date=asyncio.get_event_loop().time() + VIDEO_LIFETIME
    )
    os.remove(file); os.remove(thumb)

print("Bot started!")
app.run()
