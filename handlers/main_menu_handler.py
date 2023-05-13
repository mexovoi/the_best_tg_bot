from aiogram import Router
from aiogram.dispatcher.filters.text import Text
from aiogram.types import Message

import bot
import keyboards as kbs
import data.parsing_data as ps
import parsing.parser

router = Router()  # 1

@router.message(commands=['start'])
async def get_started(message: Message):
    await message.answer(
        "Выберете пункт меню\n"
        "Для помощи напишите /help",
        reply_markup=kbs.main_menu.get_main_menu()
    )

@router.message(commands=['help'])
async def get_help(message: Message):
    await message.answer(
        "Основные возможности бота:\n"
        "1) Просмотр новостей мира экономики и финансов\n"
        "2) Информация с сайта ЦБ РФ с экономическими показателями и текущими курсами валют\n"
        "2) Просмотр актуальных котировок акций СПБ и Московской Бирж, сырья и криптовалюты\n"
        "3) Настройка показываемой информации об акциях и возможность отслеживания котировок\n"
        "4) Инвест-идеи от автора (обновления нерегулярные и редкие)\n"
        "5) Автоматическая рассылка в 7.00 по Москве каждый день\n"
        "Для более подробной информации о возможностях работы с акциями пишите '/help_stock'\n"
        "Для более подробной информации о шаблонах '/help_pattern'"
    )


@router.message(commands=['help_stock'])
async def get_help_stock(message: Message):
    await message.answer(
        "🔷Команды '/msk_find' и '/spb_find' ищут среди названий компаний и тикеров совпадения и отправляют"
        "обратно сообщение с информацией по паттерну по умолчанию. За раз сообщение не длиннее 50 наименований\n"
    )
    await message.answer(
        "🔷Команды '/msk_add' и '/spb_add' добавляют в список отслеживаемых написанную после команды акцию при условии полного совпадения"
        "или названия или тикера (регистр на важен). В ином случае возвращается сообщение с подходязими наименованиями,"
        "лимит также 50 наименований. Например, '/msk_add yndx' добавит акцию Яндекс в отслеживаемые, а команда '/msk_add банк'"
        "вернет список со всеми акциями, где в имени есть подстрока 'банк'"
    )
    await message.answer(
        "🔷Команды '/msk_del' и '/spb_del' удалит акцию из отслеживаемых при полном совпадении тикера или названия (регистр не важен)."
        "Рекомендуется перед вызовом этой фукнции вызывать команду 'Отслеживаемые акции ...' из меню акций"
    )

@router.message(commands=['help_pattern'])
async def get_help_pattern(message: Message):
    await message.answer(
        "Примеры добавления паттернов:\n"
        "1) Добавить паттерн с текущей ценой и изменением цены за день '/msk_ch 11 0 1'\n"""
        "2) Изменить старый паттерн под номером 1 на новый с показателем только изменение за год '/msk_ch 1 6'\n"
        "3) Сделать нынешний паттерн под номером 1 паттерном по умолчанию '/msk_ch 10 1'",
        reply_markup=kbs.main_menu.get_change_notifications_menu()
    )


@router.message(Text(text="Курс $ и €"))
async def answer_bax_euro(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
            reply_markup=kbs.main_menu.get_main_menu()
        )
        return
    if '🆘' in ps.bax_rates_info[0]:
        ps.bax_rates_info.clear()
        ps.euro_rates_info.clear()
        await parsing.parser.update_cbr()
    mes =  "Вчера:          1💵 = " + ps.bax_rates_info[0] + "       1💶 = " + ps.euro_rates_info[0] + "\n"
    mes += "Позавчера: 1💵 = " + ps.bax_rates_info[1] + "       1💶 = " + ps.euro_rates_info[1]
    await message.answer(
        mes,
        reply_markup=kbs.main_menu.get_main_menu()
    )


@router.message(Text(text="Показатели ЦБ РФ"))
async def answer_values(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
            reply_markup=kbs.main_menu.get_main_menu()
        )
        return
    if '🆘' in ps.indexes_info[0]:
        await parsing.parser.update_cbr()
    mes = ""
    for row in ps.indexes_info:
        if "🆘" in row:
            mes += row + "\n"
        else:
            parts = row.split(": ")
            mes += ": 🔸".join(parts) + "🔸\n"
    await message.answer(
        mes,
        reply_markup=kbs.main_menu.get_main_menu()
    )


@router.message(Text(text="Крипта"))
async def answer_crypto(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
            reply_markup=kbs.main_menu.get_main_menu()
        )
        return
    mes = ""
    for name, info in ps.crypto_info.items():
        if (info[0] == '0.0'):
            continue
        mes += f"{name}: {info[0]}💵, дельта -  "
        if (info[1][0] == '-'):
            mes += f"🔴 {info[1]} 🔴\n"
        else:
            mes += f"🟢 {info[1]} 🟢\n"
    await message.answer(
        mes,
        reply_markup=kbs.main_menu.get_main_menu()
    )

@router.message(Text(text="Сырье"))
async def answer_goods(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
            reply_markup=kbs.main_menu.get_main_menu()
        )
        return
    mes = ""
    for name, info in ps.goods_info.items():
        if (info[0] == '0.0'):
            continue
        mes += f"{name}: {info[0]}💵, дельта -  "
        if (info[1][0] == '-'):
            mes += f"🔴 {info[1]} 🔴\n"
        else:
            mes += f"🟢 {info[1]} 🟢\n"
    await message.answer(
        mes,
        reply_markup=kbs.main_menu.get_main_menu()
    )

@router.message(Text(text="Вернуться в меню"))
async def answer_return_menu_from_news(message: Message):
    await message.answer(
        "Yes, sir",
        reply_markup=kbs.main_menu.get_main_menu()
    )

