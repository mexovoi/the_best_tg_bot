from aiogram import Router
from aiogram.dispatcher.filters.text import Text
from aiogram.types import Message

from keyboards.main_menu import get_next_news_menu, get_main_menu
import data.parsing_data as ps
import data.users_info as users_info

router = Router()  # 3

@router.message(Text(text='Новости раздела "Экономика и финансы"') or Text(text='Следующая'))
async def answer_news(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
            reply_markup=get_main_menu()
        )
        return
    usr_id = str(message.from_user.id)
    news_num = users_info.users_news_progress.get(usr_id, -1) + 1
    users_info.users_news_progress[usr_id] = news_num
    if users_info.users_news_progress[usr_id] + 1 >= ps.economic_news_info.items().__len__():
        await message.answer("Все новости на сегодня просмотрены ✅✅✅\nНачинаю с начала.")
        users_info.users_news_progress[usr_id] = 0
        news_num = 0
    name_href = None
    for item in ps.economic_news_info.items():
        name_href = item
        if news_num == 0:
            break
        news_num -= 1
    href = name_href[1]
    await message.answer(
        f"{href}",
        parse_mode="html",
        reply_markup=get_next_news_menu()
    )


@router.message(Text(text="Следующая"))
async def answer_next(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
        )
        return
    await answer_news(message)