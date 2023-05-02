from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_stocks_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Управление акциями МосБиржи")
    kb.button(text="Управление акциями ПАО СПБ Биржа")
    kb.button(text="Отслеживаемые акции МосБиржи")
    kb.button(text="Отслеживаемые акции СПБ Биржи")
    kb.button(text="Инвестиционные идеи")
    kb.button(text="Вернуться в меню")
    kb.adjust(2, 2, 2)
    return kb.as_markup(resize_keyboard=True)


