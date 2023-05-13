from aiogram import Router
from aiogram.dispatcher.filters.text import Text
from aiogram.types import Message

import bot
from data import parsing_data as ps, users_info
from keyboards import stocks_menu



router = Router()  # 2


@router.message(Text(text="Акции"))
async def answer_stock(message: Message):
    await message.answer(
        "Здесь вы можете узнать актуальную информацию о компаниях и их акциях",
        reply_markup=stocks_menu.get_stocks_menu()
    )


@router.message(commands=['msk_add'])
async def moex_add(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
        )
        return
    usr_id = str(message.from_user.id)
    if len(message.text.split()) == 1:
        return
    name = message.text.split()[1].strip().lower()
    mes = ""
    cnt = 1
    for stock in ps.stocks_msc_info.keys():
        if name in stock[0].lower() or name in stock[1].lower():
            if name == stock[0].lower() or name == stock[1].lower():
                wish_list = list(users_info.users_sets_for_msc_stocks.get(usr_id, []))
                wish_list.append(tuple(stock))
                users_info.users_sets_for_msc_stocks[usr_id] = tuple(wish_list)
                await message.answer(
                    f"Добавлено {stock[0]}({stock[1]}) в твои отслеживаемые акции.",
                    reply_markup=stocks_menu.get_stocks_menu()
                )
                return
            elif cnt < 50:
                mes += f"{cnt}) {stock[0]}({stock[1]})\n"
                cnt += 1
            elif cnt == 50:
                mes += "..."
                cnt += 1
    await message.answer(
        "По вашему запросу мы нашли вот такие акции\n" + mes,
    )


@router.message(commands=['msk_find'])
async def moex_find(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
        )
        return
    usr_id = str(message.from_user.id)
    if len(message.text.split()) == 1:
        return
    if not users_info.users_notifications_msc_stocks.get(usr_id, None):
        pattern = [0, 1, 2]
    else:
        pattern = users_info.users_notifications_msc_stocks[usr_id][0]
    name = message.text.split()[1].strip().lower()

    mes = ""
    cnt = 1
    for stock in ps.stocks_msc_info.keys():
        if name in stock[0].lower() or name in stock[1].lower():
            if cnt < 50:
                mes += f"{cnt}) {stock[0]}({stock[1]}) "
                for trait in pattern:
                    if (len(ps.stocks_msc_info[stock][trait]) == 0):
                        mes += f"🔸___"
                        continue
                    if ps.stocks_msc_info[stock][trait][0] == '-':
                        mes += f"🔸🔴{ps.stocks_msc_info[stock][trait]}🔴"
                    elif ps.stocks_msc_info[stock][trait][0] == '+':
                        mes += f"🔸🟢{ps.stocks_msc_info[stock][trait]}🟢"
                    else:
                        mes += f"🔸{ps.stocks_msc_info[stock][trait]}"
                mes += "\n"
                cnt += 1
            elif cnt == 50:
                mes += "..."
                cnt += 1
    await message.answer(
        "По вашему запросу мы нашли вот такие акции\n" + mes,
        reply_markup=stocks_menu.get_stocks_menu()
    )


@router.message(commands=['msk_del'])
async def moex_delete(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
        )
        return
    if len(message.text.split()) == 1:
        return
    usr_id = str(message.from_user.id)
    name = message.text.split()[1].strip().lower()
    if usr_id in users_info.users_sets_for_msc_stocks.keys():
        wish_list = list(users_info.users_sets_for_msc_stocks[usr_id])
    else:
        wish_list = []
    for i in range(len(wish_list)):
        if name == wish_list[i][0].lower() or name == wish_list[i][1].lower():
            await message.answer(
                f"Акция {wish_list[i][0]}({wish_list[i][1]}) удалена из отслеживаемых",
                reply_markup=stocks_menu.get_stocks_menu()
            )
            del wish_list[i]
            users_info.users_sets_for_msc_stocks[usr_id] = tuple(wish_list)
            return
    await message.answer(
        f"Не найдено совпадений с акцией {name}",
        reply_markup=stocks_menu.get_stocks_menu()
    )

@router.message(Text(text="Управление акциями МосБиржи"))
async def answer_msc_stocks(message: Message):
    await message.answer(
        "Введите частичное название акции или ее тикер.\n"
        "Шаблон для ввода для поиска - '/msk_find ____'\n"
        "Шаблон для ввода для добавления в подписки - '/msk_add ____'\n"
        "Шаблон для удаления из подписок - '/msk_del ____'",
        reply_markup=stocks_menu.get_stocks_menu()
    )


@router.message(Text(text="Отслеживаемые акции МосБиржи"))
async def answer_followed_msk_stocks(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
        )
        return
    usr_id = str(message.from_user.id)
    if usr_id not in users_info.users_sets_for_msc_stocks.keys():
        await message.answer(
            "Список отслеживаемых акций МосБиржи пуст",
            reply_markup=stocks_menu.get_stocks_menu()
        )
        return
    if not users_info.users_notifications_msc_stocks.get(usr_id, None):
        pattern = [0, 1, 2]
    else:
        pattern = users_info.users_notifications_msc_stocks[usr_id][0]
    cnt = 1
    if len(users_info.users_sets_for_msc_stocks[usr_id]) == 0:
        await message.answer(
            "Список отслеживаемых акций пуст",
            reply_markup=stocks_menu.get_stocks_menu()
        )
        return
    mes = ""
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
        if cnt % 50 == 0:
            await message.answer(
                mes
            )
            mes = ""
    await message.answer(
        mes
    )

@router.message(commands=['spb_add'])
async def moex_add(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
        )
        return
    usr_id = str(message.from_user.id)
    if len(message.text.split()) == 1:
        return
    name = message.text.split()[1].strip().lower()
    mes = ""
    cnt = 1
    for stock in ps.stocks_spb_info.keys():
        if name in stock[0].lower() or name in stock[1].lower():
            if name == stock[0].lower() or name == stock[1].lower():
                wish_list = list(users_info.users_sets_for_spb_stocks.get(usr_id, []))
                wish_list.append(tuple(stock))
                users_info.users_sets_for_spb_stocks[usr_id] = tuple(wish_list)
                await message.answer(
                    f"Добавлено {stock[0]}({stock[1]}) в твои отслеживаемые акции.",
                    reply_markup=stocks_menu.get_stocks_menu()
                )
                return
            elif cnt < 50:
                mes += f"{cnt}) {stock[0]}({stock[1]})\n"
                cnt += 1
            elif cnt == 50:
                mes += "..."
                cnt += 1
    await message.answer(
        "По вашему запросу мы нашли вот такие акции\n" + mes,
    )


@router.message(commands=['spb_find'])
async def moex_find(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
        )
        return
    usr_id = str(message.from_user.id)
    if len(message.text.split()) == 1:
        return
    if not users_info.users_notifications_spb_stocks.get(usr_id, None):
        pattern = [0, 1, 2]
    else:
        pattern = users_info.users_notifications_spb_stocks[usr_id][0]
    name = message.text.split()[1].strip().lower()

    mes = ""
    cnt = 1
    for stock in ps.stocks_spb_info.keys():
        if name in stock[0].lower() or name in stock[1].lower():
            if cnt < 50:
                mes += f"{cnt}) {stock[0]}({stock[1]}) "
                for trait in pattern:
                    if (len(ps.stocks_spb_info[stock][trait]) == 0):
                        mes += f"🔸___"
                        continue
                    if ps.stocks_spb_info[stock][trait][0] == '-':
                        mes += f"🔸🔴{ps.stocks_spb_info[stock][trait]}🔴"
                    elif ps.stocks_spb_info[stock][trait][0] == '+':
                        mes += f"🔸🟢{ps.stocks_spb_info[stock][trait]}🟢"
                    else:
                        mes += f"🔸{ps.stocks_spb_info[stock][trait]}"
                mes += "\n"
                cnt += 1
            elif cnt == 50:
                mes += "..."
                cnt += 1
    await message.answer(
        "По вашему запросу мы нашли вот такие акции\n" + mes,
        reply_markup=stocks_menu.get_stocks_menu()
    )


@router.message(commands=['spb_del'])
async def moex_delete(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
        )
        return
    if len(message.text.split()) == 1:
        return
    usr_id = str(message.from_user.id)
    name = message.text.split()[1].strip().lower()
    if usr_id in users_info.users_sets_for_spb_stocks.keys():
        wish_list = list(users_info.users_sets_for_spb_stocks[usr_id])
    else:
        wish_list = []
    for i in range(len(wish_list)):
        if name == wish_list[i][0].lower() or name == wish_list[i][1].lower():
            await message.answer(
                f"Акция {wish_list[i][0]}({wish_list[i][1]}) удалена из отслеживаемых",
                reply_markup=stocks_menu.get_stocks_menu()
            )
            del wish_list[i]
            users_info.users_sets_for_spb_stocks[usr_id] = tuple(wish_list)
            return
    await message.answer(
        f"Не найдено совпадений с акцией {name}",
        reply_markup=stocks_menu.get_stocks_menu()
    )


@router.message(Text(text="Управление акциями ПАО СПБ Биржа"))
async def answer_spb_stocks(message: Message):
    await message.answer(
        "Введите частичное название акции или ее тикер.\n"
        "Шаблон для ввода для поиска - '/spb_find ____'\n"
        "Шаблон для ввода для добавления в подписки - '/spb_add ____'\n"
        "Шаблон для удаления из подписок - '/spb_del ____'",
        reply_markup=stocks_menu.get_stocks_menu()
    )


@router.message(Text(text="Отслеживаемые акции СПБ Биржи"))
async def answer_followed_spb_stocks(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
        )
        return
    usr_id = str(message.from_user.id)
    if usr_id not in users_info.users_sets_for_spb_stocks.keys():
        await message.answer(
            "Список отслеживаемых акций МосБиржи пуст",
            reply_markup=stocks_menu.get_stocks_menu()
        )
        return
    if not users_info.users_notifications_spb_stocks.get(usr_id, None):
        pattern = [0, 1, 2]
    else:
        pattern = users_info.users_notifications_spb_stocks[usr_id][0]
    cnt = 1
    if len(users_info.users_sets_for_spb_stocks[usr_id]) == 0:
        await message.answer(
            "Список отслеживаемых акций пуст",
            reply_markup=stocks_menu.get_stocks_menu()
        )
        return
    mes = ""
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
        if cnt % 50 == 0:
            await message.answer(
                mes
            )
            mes = ""
    await message.answer(
        mes
    )

@router.message(Text(text="Инвестиционные идеи"))
async def answer_invest_ideas(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
        )
        return
    mes = ""
    cnt = 1
    for idea in ps.invest_ideas_info.keys():
        mes += f'{cnt}) {idea.strip()}:\n{ps.invest_ideas_info[idea][0]}\n'\
               f'{ps.invest_ideas_info[idea][1]}\n{ps.invest_ideas_info[idea][2]}'
        cnt += 1
        await message.answer(
            mes
        )
        mes = ""