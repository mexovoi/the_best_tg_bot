import aioschedule
import asyncio

import bot
from data import parsing_data as ps, users_info
from parsing import parser


async def send_news():
    mes = "📈📉📈\tЕжедневная сводка новостей\t📉📈📉\n\n"
    for news in ps.economic_news_info.keys():
        mes += "☑️ " + news + "\n"
    for usr_id in users_info.users_news_progress:
        await bot.tg_bot.send_message(int(usr_id), mes)


async def send_msc_stocks():
    for usr_id in users_info.users_sets_for_msc_stocks:
        if not users_info.users_notifications_msc_stocks.get(usr_id, None):
            pattern = [0, 1, 2]
        else:
            pattern = users_info.users_notifications_msc_stocks[usr_id][0]
        mes = "📈📉📈\tЕжедневная сводка по акциям на Бирже Москвы\n"
        cnt = 1
        for stock in users_info.users_sets_for_msc_stocks[usr_id]:
            mes += f"{cnt}) {stock[0]}({stock[1]}) "
            for trait in pattern:
                if ps.stocks_msc_info[stock][trait][0] == '-':
                    mes += f"🔸🔴{ps.stocks_msc_info[stock][trait]}🔴"
                elif ps.stocks_msc_info[stock][trait][0] == '+':
                    mes += f"🔸🟢{ps.stocks_msc_info[stock][trait]}🟢"
                else:
                    mes += f"🔸{ps.stocks_msc_info[stock][trait]}"
            mes += "\n"
            cnt += 1
        await bot.tg_bot.send_message(int(usr_id), mes)


async def send_spb_stocks():
    for usr_id in users_info.users_sets_for_spb_stocks:
        if not users_info.users_notifications_spb_stocks.get(usr_id, None):
            pattern = [0, 1, 2]
        else:
            pattern = users_info.users_notifications_spb_stocks[usr_id][0]
        mes = "📈📉📈\tЕжедневная сводка по акциям на Бирже СПБ\n"
        cnt = 1
        for stock in users_info.users_sets_for_spb_stocks[usr_id]:
            mes += f"{cnt}) {stock[0]}({stock[1]}) "
            for trait in pattern:
                if ps.stocks_spb_info[stock][trait][0] == '-':
                    mes += f"🔸🔴{ps.stocks_spb_info[stock][trait]}🔴"
                elif ps.stocks_spb_info[stock][trait][0] == '+':
                    mes += f"🔸🟢{ps.stocks_spb_info[stock][trait]}🟢"
                else:
                    mes += f"🔸{ps.stocks_spb_info[stock][trait]}"
            mes += "\n"
            cnt += 1
        await bot.tg_bot.send_message(int(usr_id), mes)


async def send_notifications() -> None:
    ps.updating = True
    await parser.update_all()
    ps.updating = False

    await send_news()
    await send_msc_stocks()
    await send_spb_stocks()

async def scheduler():
    aioschedule.every().day.at("07:00").do(send_notifications)
    aioschedule.every().day.at("19:00").do(send_notifications)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(10)

