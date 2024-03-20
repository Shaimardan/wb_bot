from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

# main = [
#     [KeyboardButton(text='Получить информацию по товару', callback_data='get_info')]
# ]

kb = [
    [
        KeyboardButton(text="Получить информацию по товару")
    ],
]
main = ReplyKeyboardMarkup(
    keyboard=kb
)


subscribe_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подписаться', callback_data='subscribe')],
])

subscribe_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отписаться', callback_data='subscribe')],
])
