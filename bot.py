from config import TelegramBotAPItoken
from aiogram.utils.markdown import hunderline, hlink
from aiogram import Bot, Dispatcher, executor, types
from sql import SQL
import logging
import asyncio
import main

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TelegramBotAPItoken, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

db = SQL('db.db')


@dp.message_handler(commands=["start", "menu"])
async def start_command(message: types.Message):
    await message.answer(text=f"This is bot for retrieving news from HLTV.org."
                              f" It is created by @Wyrierit "
                              f" using "
                              f"video lessons and Python libraries (requests, aiogram, BeautifulSoup4)."
                              f" \n \n Available commands: \n"
                              f"/subscribe — this will activate your subscription \n"
                              f"/unsubscribe — you will no longer receive news")


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id)
    else:
        db.update_subscription(message.from_user.id, True)

    await message.answer("You've successfully subscribed! Stay tuned for news.")


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id, False)
        await message.answer("You weren't a subscriber")
    else:
        db.update_subscription(message.from_user.id, False)
        await message.answer("You've successfully unsubscribed! Goodbye and have a good day 👋🏻")


async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        fresh_news = main.newnews()
        subscriptions = db.get_subscriptions()
        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                """news = f"{v['news_datetime']}" \
                       f"{v['news_title']}\n" \
                       f"\n" \
                       f"{v['news_description']}\n" \
                       f"\n" \
                       f"Read more: {v['news_url']}\n"""

                news = f"{hunderline(v['news_datetime'])} \n" \
                       f"{hlink(v['news_title'], v['news_url'])} \n \n" \
                       f"{v['news_description']}\n \n" \
                       f"Read more: {v['news_url']}"
            for s in subscriptions:
                await bot.send_message(s[1], news, disable_notification=True, disable_web_page_preview=True)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(5))
    executor.start_polling(dp, skip_updates=True)
