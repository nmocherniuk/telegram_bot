import asyncio
import os
from telegram import Bot
from datetime import datetime
from zoneinfo import ZoneInfo  # <-- нове

TOKEN = os.getenv("TOKEN")
USER_ID = int(os.getenv("USER_ID"))

bot = Bot(token=TOKEN)

KYIV_TZ = ZoneInfo("Europe/Kyiv")

async def send_reminder():
    message = "🔥 Don't forget to send a message on TikTok today!"
    try:
        await bot.send_message(chat_id=USER_ID, text=message)
    except Exception as e:
        print(f"Error sending message: {e}")

SEND_HOURS = [21]
MINUTE_TO_SEND = 0

already_sent = set()

async def main():
    print("Bot started...")
    while True:
        now = datetime.now(KYIV_TZ)
        current_time = (now.hour, now.minute)

        if now.minute == MINUTE_TO_SEND and now.hour in SEND_HOURS:
            if current_time not in already_sent:
                await send_reminder()
                already_sent.add(current_time)
                print(f"Reminder sent at {now.hour:02d}:{now.minute:02d} (Kyiv time)")
        else:
            if len(already_sent) == len(SEND_HOURS):
                already_sent.clear()

        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
