from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_kb():
    kb_list = [[InlineKeyboardButton(callback_data='previous', text='Предыдущий заказ')],
               [InlineKeyboardButton(callback_data='next', text='Следующий заказ')]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
