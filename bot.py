import asyncio
import base64
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

# Telegram API Details (my.telegram.org se lein)
API_ID = 38215355
API_HASH = "3f095c170be8c744b8f3d7f9c75ae544"  
BOT_TOKEN = "8700557784:AAG8jS0Ua6PiQLj14ct6iVFo15MveDN8WRE"  # @BotFather se lein

# Channels Setup
FORCE_SUB_CHANNEL = -1003964032718  # Aapka Channel ID
FORCE_SUB_LINK = "https://t.me/all_anime_update"  # Channel Link
DB_CHANNEL = -1004487298929
# Private Storage Channel (Jahan files save hongi)

# Custom Banner Image URL
BANNER_IMAGE_URL = "https://telegra.ph/file/your_image_link.jpg" 

app = Client("my_file_store_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def encode_data(data: str) -> str:
    return base64.b64encode(data.encode('ascii')).decode('ascii').strip("=")

def decode_data(data: str) -> str:
    padding = '=' * (4 - len(data) % 4)
    return base64.b64decode((data + padding).encode('ascii')).decode('ascii')


@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user_id = message.from_user.id
    args = message.text.split(maxsplit=1)
    
    # 1. Force Subscribe Check
    try:
        await client.get_chat_member(FORCE_SUB_CHANNEL, user_id)
    except UserNotParticipant:
        start_param = args[1] if len(args) > 1 else ""
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Join Channel 1", url=FORCE_SUB_LINK)],
            [InlineKeyboardButton("🔄 Try Again", url=f"https://t.me/{client.me.username}?start={start_param}")]
        ])
        return await message.reply_text(
            f"Hey **{message.from_user.first_name}**,\n\n"
            "Please Join All My Update Channels To Use Me!", 
            reply_markup=buttons
        )

    # 2. Normal /start command
    if len(args) == 1:
        return await message.reply_text("👋 Welcome! Mujhe koi bhi file/post bhein, main link bana dunga.")

    # 3. File/Link Delivery + Auto Delete Logic
    try:
        base64_string = args[1]
        decoded_id = decode_data(base64_string)
        msg_id = int(decoded_id.split("_")[1])

        # Channel Link + Custom Photo Caption
        target_link = "https://t.me/+-3si6P4o-8QwNDNl"
        caption_text = f"**Channel Link** 🔗 👇👇\n\n{target_link}\n{target_link}"
        
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("📟 UPDATE CHANNEL", url=FORCE_SUB_LINK)]
        ])

        # Photo + Link Send
        msg1 = await message.reply_photo(
            photo=BANNER_IMAGE_URL,
            caption=caption_text,
            reply_markup=reply_markup
        )
        
        # Warning Notice Send
        warning_text = (
            "**THIS FILE WILL BE DELETED IN 5 MINUTES. "
            "PLEASE SAVE OR FORWARD IT TO YOUR SAVED MESSAGES BEFORE IT GETS DELETED.**"
        )
        msg2 = await message.reply_text(warning_text)

        # 5 Minute (300 Seconds) Auto Delete Timer
        await asyncio.sleep(300)
        try:
            await msg1.delete()
            await msg2.delete()
        except Exception:
            pass

    except Exception:
        await message.reply_text("⚠️ Link invalid hai ya expired ho chuka hai.")


# 4. Link Generator (Admin Only File/Post Upload)
@app.on_message(filters.private & ~filters.command("start"))
async def store_file(client, message):
    # Message ko Storage channel par copy karna
    sent_msg = await message.copy(chat_id=DB_CHANNEL)
    
    # Message ID Encode karke Link banana
    string_format = f"file_{sent_msg.id}"
    base64_code = encode_data(string_format)
    share_link = f"https://t.me/{client.me.username}?start={base64_code}"

    await message.reply_text(
        f"✅ **Link Stored Successfully!**\n\n"
        f"🔗 **Shareable Link:**\n`{share_link}`",
        disable_web_page_preview=True
    )

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
