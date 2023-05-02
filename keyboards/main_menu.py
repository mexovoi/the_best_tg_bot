from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Курс $ и €")
    kb.button(text="Показатели ЦБ РФ")
    kb.button(text="Акции")
    kb.button(text="Изменить подписки")
    kb.button(text="Крипта")
    kb.button(text="Сырье")
    kb.button(text='Новости раздела "Экономика и финансы"')
    kb.adjust(2, 2, 2, 1)
    return kb.as_markup(resize_keyboard=True)


def get_next_news_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Следующая")
    kb.button(text="Вернуться в меню")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_change_notifications_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Новости")
    kb.button(text="Напоминалка")
    kb.button(text="Изменить паттерны Московской Биржи")
    kb.button(text="Изменить паттерны СПБ Биржи")
    kb.button(text="Вернуться в меню")
    kb.adjust(2, 2, 1)
    return kb.as_markup(resize_keyboard=True)