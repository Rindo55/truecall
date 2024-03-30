import re
import traceback
from pyrogram import Client, filters, types
from pyrogram.types import Message
from bot.config import Buttons
from bot.utils import search_number
import html2text
import json
import subprocess
@Client.on_message(
    filters.regex(f"{Buttons.trucaller_info_text}") & filters.private & filters.incoming
)
async def truecaller_info(client: Client, message: Message):
    ask = await message.chat.ask(
        text="Send me the number you want to search for.\n\n"
        "Example (Format): `+919876543210`\n"
        "Only Indian numbers are supported.\n\n",
        filters=filters.text,
        timeout=3600,
    )
    print(ask)
    regex = r"^\+?[1-9]\d{1,14}$"

    if not re.search(regex, ask.text):
        await message.reply_text("Invalid number! Please try again and see the example.")
        return

    txt = await message.reply_text("Searching for the number...")

    try:
        result = await search_number(ask.text)
    except Exception as e:
        await message.reply_text(f"Error : `{e}`")
        return
    try:
        Score = float(result["data"]["data"][0]["score"] if result["data"]["data"][0]["score"] else None)
        if Score != None:
            score_Percent = Score*100
        else:
            pass
        kayo = result["data"]
        text = f"""Information found on Truecaller for {ask.text}:
        
Name: {result["data"]["data"][0]["name"]}
Score: {score_Percent}%
Carrier: {result["data"]["data"][0]["phones"][0]["carrier"] if result["data"]["data"][0]["phones"] else None}
Address: {result["data"]["data"][0]["addresses"][0]["city"] if result["data"]["data"][0]["addresses"] else None} 
Email: {result["data"]["data"][0]["internetAddresses"][0]["id"] if result["data"]["data"][0]["internetAddresses"] else None}
"""
        await txt.edit(text=f"{text}\n{kayo}", disable_web_page_preview=True)
    except Exception as e:
        traceback.print_exc()
        await txt.edit(f"Error: {e}")

@Client.on_message(filters.private)
async def lookup_number(bot, message):
    if message.text.startswith("/lookup"):
        input_number = message.text.replace("/lookup", "").strip()
        number = ''.join(filter(str.isdigit, input_number))
        
        if len(number) >= 7:  # Assuming Indian phone numbers have at least 10 digits
            output = subprocess.check_output(['truecallerjs', '-s', '+' + number, '--json']).decode('utf-8')
    
            await message.reply(output)
        else:
            await message.reply("Invalid phone number format.")
    else:
        await message.reply("Send /lookup followed by the phone number to look up.")

def html_to_markdown(html_content):
    converter = html2text.HTML2Text()
    converter.body_width = 0  # Set body_width to 0 to disable line wrapping
    return converter.handle(html_content)
