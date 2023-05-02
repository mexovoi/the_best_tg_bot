import asyncio
from aiogram import Bot, Dispatcher

import sending_messages
from parsing import parser
from config import TOKEN
from handlers import main_menu_handler, news_handler, stocks_handler, notifications_handler

tg_bot = Bot(token=TOKEN)
dp = Dispatcher()

# Запуск бота
async def main():
    dp.include_router(main_menu_handler.router)
    dp.include_router(stocks_handler.router)
    dp.include_router(news_handler.router)
    dp.include_router(notifications_handler.router)

    await parser.update_all()
    asyncio.create_task(sending_messages.scheduler())

    # Запускаем бота и пропускаем все накопленные входящие
    await tg_bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(tg_bot)

if __name__ == "__main__":
    asyncio.run(main())