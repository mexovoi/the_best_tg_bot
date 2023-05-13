from aiogram import Router
from aiogram.dispatcher.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove

import bot
import data.parsing_data as ps
import data.users_info as usr_info
import keyboards as kbs

router = Router()  # 4

@router.message(Text(text="Изменить подписки"))
async def change_notifications(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
            reply_markup=kbs.main_menu.get_change_notifications_menu()
        )
        return
    await message.answer(
        "Выберете, что будем менять",
        reply_markup=kbs.main_menu.get_change_notifications_menu()
    )

@router.message(Text(text="Новости"))
async def change_news_notifications_mode(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
            reply_markup=kbs.main_menu.get_change_notifications_menu()
        )
        return
    usr_id = str(message.from_user.id)
    if usr_id not in usr_info.users_news_progress:
        usr_info.users_news_progress[usr_id] = True
        await message.answer(
            "🟢 Оповещение о новостях включено 🟢",
            reply_markup=kbs.main_menu.get_change_notifications_menu()
        )
    else:
        del usr_info.users_news_progress[usr_id]
        await message.answer(
            "🔴 Оповещение о новостях выключено 🔴",
            reply_markup=kbs.main_menu.get_change_notifications_menu()
        )


@router.message(Text(text="Напоминалка"))
async def notification_message(message: Message):
    await message.answer(
        "🔷Для составления паттерна нужно ввести последовательность чисел, каждая из которых обозначает показатель, который вы хотите отслеживать."
        "Если вы хотите изменить паттерны МосБиржи, тогда сначала идет команда '/msk_ch', для СПБ Биржи '/spb_ch' далее числа"
    )
    await message.answer(
        "🔷Обозначения для Биржы СПБ:\n0 - цена\n1 - изменение цены за день\n2 - объем сделок в $\n3 - изменение за неделю\n"
        "4 - изменение за месяц\n5 - изменение с начала года\n6 - изменение за год"
    )
    await message.answer(
        "🔷Обозначения для Московской Биржы:\n0 - цена\n1 - изменение цены за день\n2 - объем сделок в $\n3 - изменение за неделю\n"
        "4 - изменение за месяц\n5 - изменение с начала года\n6 - изменение за год\n7 - капитализация в ₽\n8 - капитализация в $"
    )
    await message.answer(
        "🔷Для добавления нового паттерна пишите цифру 11 после команды '/msk_ch 11 (цифры через пробел)'\n"
        "🔷Для изменения паттерна по умолчанию пишите цифру 10 после команды, а затем номер желаемого паттерна по умолчанию '/spb_ch 10 (номер нового паттерна по умолчанию)'\n"
        "🔷Для изменения старого паттерна пишите после команды номер изменяемого паттерна '/msk_ch (номер паттерна) (последовательность)'"
        "🔷Пример правильного паттерна добавления можно смотреть в '/help_pattern'",
        reply_markup=kbs.main_menu.get_change_notifications_menu()
    )



async def check_indexes_moex(parameters: list) -> bool:
    for elem in parameters:
        if not elem.isnumeric():
            return True
        if not 0 <= int(elem) <= 8:
            return True
    return False



@router.message(Text(text="Изменить паттерны Московской Биржи"))
async def change_msk_stocks_notifications_patterns(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
            reply_markup=kbs.main_menu.get_change_notifications_menu()
        )
        return
    usr_id = str(message.from_user.id)
    usr_info.users_notifications_msc_stocks[usr_id] = usr_info.users_notifications_msc_stocks.get(usr_id, tuple())

    notification_tuple = usr_info.users_notifications_msc_stocks[usr_id]

    if len(notification_tuple) >= 1:
        idx = 0
        mes = f"По умолчанию: {idx}) {notification_tuple[0]}\nСохраненные(Всего паттернов максимум 10):\n"
        for another_pattern in notification_tuple[1:]:
            idx += 1
            mes += f"{idx}) {another_pattern}\n"
        await message.answer(
            mes,
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        mes = "Паттерны не были добавлены.\nСамое время вызвать напоминалочку и создать свой первый паттерн."
        await message.answer(
            mes,
            reply_markup=kbs.main_menu.get_change_notifications_menu()
        )



@router.message(commands=['msk_ch'])
async def change_patterns_msk_stocks_command(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
            reply_markup=kbs.main_menu.get_change_notifications_menu()
        )
        return
    params = message.text.split()
    pattern_idx = params[1]
    pattern_params = params[2:]

    if not pattern_idx.isnumeric():
        return
    elif int(pattern_idx) == 112:
        await message.answer(
            "Выход в меню редактирования",
            reply_markup=kbs.main_menu.get_change_notifications_menu()
        )
        return

    usr_id = str(message.from_user.id)
    usr_info.users_notifications_msc_stocks[usr_id] = usr_info.users_notifications_msc_stocks.get(usr_id, tuple())

    patterns_list = list(usr_info.users_notifications_msc_stocks[usr_id])

    if int(pattern_idx) == 10:
        if len(pattern_params) > 1:
            patterns_list[int(pattern_params[0])]  = [int(i) for i in pattern_params[1:]]
            usr_info.users_notifications_msc_stocks[usr_id] = tuple(patterns_list)
            await message.answer(
                "Операция успешно завершена",
                reply_markup=kbs.main_menu.get_change_notifications_menu()
            )
            return

    if await check_indexes_moex(pattern_params):
        await message.answer(
            "Что-то пошло не так. 🔴Ошибка🔴"
        )
        await change_msk_stocks_notifications_patterns(message)
        return


    if not (0 <= int(pattern_idx) < len(patterns_list) or int(pattern_idx) == 11):
        await message.answer(
            "Что-то пошло не так. 🔴Ошибка🔴"
        )
        await change_msk_stocks_notifications_patterns(message)
        return

    if len(pattern_params) == 0:
        if 0 <= int(pattern_idx) < len(patterns_list):
            del patterns_list[int(pattern_idx)]
            usr_info.users_notifications_msc_stocks[usr_id] = tuple(patterns_list)
            await message.answer(
                "Операция успешно завершена",
                reply_markup=kbs.main_menu.get_change_notifications_menu()
            )
        else:
            await message.answer(
                "Что-то пошло не так. 🔴Ошибка🔴"
            )
            await change_msk_stocks_notifications_patterns(message)
        return
    if len(patterns_list) >= 10:
        await message.answer(
            "🔴Превышен лимит паттернов🔴",
            reply_markup=kbs.main_menu.get_change_notifications_menu()
        )
        await change_msk_stocks_notifications_patterns(message)
        return
    if int(pattern_idx) == 11:
        patterns_list.append([int(param) for param in pattern_params])
    else:
        patterns_list[int(pattern_idx)] = [int(param) for param in pattern_params]
    usr_info.users_notifications_msc_stocks[usr_id] = tuple(patterns_list)
    await message.answer(
        "Операция успешно завершена",
        reply_markup=kbs.main_menu.get_change_notifications_menu()
    )



async def check_indexes_spb(parameters: list) -> bool:
    for elem in parameters:
        if not elem.isnumeric():
            return True
        if not 0 <= int(elem) <= 8:
            return True
    return False



@router.message(Text(text="Изменить паттерны СПБ Биржи"))
async def change_spb_stocks_notifications_patterns(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
            reply_markup=kbs.main_menu.get_change_notifications_menu()
        )
        return
    usr_id = str(message.from_user.id)
    usr_info.users_notifications_spb_stocks[usr_id] = usr_info.users_notifications_spb_stocks.get(usr_id, tuple())

    notification_tuple = usr_info.users_notifications_spb_stocks[usr_id]

    if len(notification_tuple) >= 1:
        idx = 0
        mes = f"По умолчанию: {idx}) {notification_tuple[0]}\nСохраненные(Всего паттернов максимум 10):\n"
        for another_pattern in notification_tuple[1:]:
            idx += 1
            mes += f"{idx}) {another_pattern}\n"
        await message.answer(
            mes,
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        mes = "Паттерны не были добавлены.\nСамое время вызвать напоминалочку и создать свой первый паттерн."
        await message.answer(
            mes,
            reply_markup=kbs.main_menu.get_change_notifications_menu()
        )


@router.message(commands=['spb_ch'])
async def change_patterns_spb_stocks_command(message: Message):
    if ps.updating:
        await message.answer(
            "Идет обновление, повторите запрос через ~10 секунд",
            reply_markup=kbs.main_menu.get_change_notifications_menu()
        )
        return
    params = message.text.split()
    pattern_idx = params[1]
    pattern_params = params[2:]

    if not pattern_idx.isnumeric():
        return
    elif int(pattern_idx) == 112:
        await message.answer(
            "Выход в меню редактирования",
            reply_markup=kbs.main_menu.get_change_notifications_menu()
        )
        return

    usr_id = str(message.from_user.id)
    usr_info.users_notifications_spb_stocks[usr_id] = usr_info.users_notifications_spb_stocks.get(usr_id, tuple())

    patterns_list = list(usr_info.users_notifications_spb_stocks[usr_id])

    if int(pattern_idx) == 10:
        if len(pattern_params) > 1:
            patterns_list[int(pattern_params[0])]  = [int(i) for i in pattern_params[1:]]
            usr_info.users_notifications_spb_stocks[usr_id] = tuple(patterns_list)
            await message.answer(
                "Операция успешно завершена",
                reply_markup=kbs.main_menu.get_change_notifications_menu()
            )
            return

    if await check_indexes_spb(pattern_params):
        await message.answer(
            "Что-то пошло не так. Ошибка"
        )
        await change_spb_stocks_notifications_patterns(message)
        return


    if not (0 <= int(pattern_idx) < len(patterns_list) or int(pattern_idx) == 11):
        await message.answer(
            "Что-то пошло не так. Ошибка"
        )
        await change_spb_stocks_notifications_patterns(message)
        return

    if len(pattern_params) == 0:
        if 0 <= int(pattern_idx) < len(patterns_list):
            del patterns_list[int(pattern_idx)]
            usr_info.users_notifications_spb_stocks[usr_id] = tuple(patterns_list)
            await message.answer(
                "Операция успешно завершена",
                reply_markup=kbs.main_menu.get_change_notifications_menu()
            )
        else:
            await message.answer(
                "Что-то пошло не так. Ошибка"
            )
            await change_spb_stocks_notifications_patterns(message)
        return
    if len(patterns_list) >= 10:
        await message.answer(
            "🔴Превышен лимит паттернов🔴",
            reply_markup=kbs.main_menu.get_change_notifications_menu()
        )
        await change_spb_stocks_notifications_patterns(message)
        return
    if int(pattern_idx) == 11:
        patterns_list.append([int(param) for param in pattern_params])
    else:
        patterns_list[int(pattern_idx)] = [int(param) for param in pattern_params]
    usr_info.users_notifications_spb_stocks[usr_id] = tuple(patterns_list)
    await message.answer(
        "Операция успешно завершена",
        reply_markup=kbs.main_menu.get_change_notifications_menu()
    )

