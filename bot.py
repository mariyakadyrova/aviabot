
import discord
from discord.ext import commands, tasks
from datetime import datetime
import pytz
from discord.ui import View, Button

from google_docs_utils import create_google_doc


TOKEN = ""    # Тут указать токен от бота

CHANNEL_ID = ""  # ← сюда бот шлёт сообщения, поменять на id канала air

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# cюда будем сохранять ссылку на последний документ
doc_url = None
last_created_date = None


@bot.event
async def on_ready():
    print(f"✅ Бот запущен как ✅ Бот запущен как✅ Бот запущен как✅ Бот запущен как {bot.user}")
    # monday_doc_creator.start()
    global doc_url
    doc_url = create_google_doc()
    print(f"📝 Док для теста создан: {doc_url}")

    friday_14_reminder.start()
    friday_18_message.start()

#  ПЯТНИЦА в 14:00 – КНОПКА НА ДОКУ
@tasks.loop(minutes=1)
async def friday_14_reminder():
    global doc_url
    tz = pytz.timezone("Asia/Almaty")
    now = datetime.now(tz)

    if now.weekday() == 4 and now.hour == 18 and now.minute == 5:  #тут могу поменять дату
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            if doc_url:
                button = Button(label="📌 💡Демочка-Напоминание", url=doc_url, style=discord.ButtonStyle.link)
                view = View()
                view.add_item(button)
                await channel.send("ДЕМО, ВПЕРЕД !!! 👇", view=view)
            else:
                await channel.send(" Документ на эту неделю ещё не создан.")
        else:
            print("❌⚠️ SOOOOOS ⚠️ ⚠️ ⚠️ Канал не найден")


#  ПЯТНИЦА в 18:00 – СООБЩЕНИЕ, может поменять на 18:30 ?
@tasks.loop(minutes=1)
async def friday_18_message():
    tz = pytz.timezone("Asia/Almaty")
    now = datetime.now(tz)

    if now.weekday() == 4 and now.hour == 18 and now.minute == 6:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("✨пятничная напоминалка провести выходные круто!🎉")
        else:
            print("❌ Канал не найден")


# летс го
bot.run(TOKEN)
