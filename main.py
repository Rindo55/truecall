from bot import Bot

from pyrogram import Client, filters
import subprocess

bot = Client("your_bot_token")

@bot.on_message(filters.private)
async def lookup_number(bot, message):
    if message.text.startswith("/lookup"):
        number = message.text.replace("/lookup", "").strip()
        if number.isdigit():
            output = subprocess.check_output(['truecallerjs', '-s', number, '--json']).decode('utf-8')
            await message.reply(output)
        else:
            await message.reply("Invalid phone number format.")
    else:
        await message.reply("Send /lookup followed by the phone number to look up.")

bot.run()

if __name__ == '__main__':
    Bot().run()
