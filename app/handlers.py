import asyncio

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import app.keyboards as kb
from app.database.requests import add_subscribe_id
from aiogram.fsm.context import FSMContext
from aiogram import types

from main import bot
from wb.wb_utils import ProductQuery, WildberriesProductInfo

router = Router()
task = {}
id_list = []


@router.message(CommandStart())
@router.callback_query(F.data == 'to_main')
async def cmd_start(message: Message | CallbackQuery):
    if isinstance(message, Message):
        await message.answer("Добро пожаловать!",
                             reply_markup=kb.main)
    else:
        await message.answer('Вы вернулись на главную')
        await message.message.answer("Добро пожаловать!",
                                     reply_markup=kb.main)


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_subscribe_button(product_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подписаться", callback_data=f"subscribe_{product_id}")],
    ])


@router.message()
async def receive_product_id(message: types.Message, state: FSMContext):
    if await state.get_state() == ProductQuery.waiting_for_product_id:
        product_id = message.text

        product_info_instance = WildberriesProductInfo(product_id)
        product_info = product_info_instance.fetch_product_info()
        message_text = f"<b>Название</b>: {product_info['name']}\n" \
                       f"<b>Артикул</b>: <code>{product_info['articul']}</code>\n" \
                       f"<b>Цена</b>: {.2} руб.\n" \
                       f"<b>Рейтинг</b>: {product_info['rating']} ⭐\n"

        await message.answer(text=message_text, parse_mode='HTML',
                             reply_markup=create_subscribe_button(product_id))
        await state.clear()
    elif message.text == "Получить информацию по товару":
        await message.answer("Привет! Отправьте мне артикул товара.")
        await state.set_state(ProductQuery.waiting_for_product_id)


@router.callback_query(lambda cq: cq.data.startswith('subscribe_'))
async def handle_subscribe_callback(callback_query: CallbackQuery):
    product_id = callback_query.data.split('_')[1]
    text = f"Вы подписались на уведомления о товаре с ID: {product_id}"
    await add_subscribe_id(callback_query.from_user.id, product_id)
    if product_id in task and not task[product_id].cancelled():
        task[product_id].cancel()

    task[product_id] = asyncio.create_task(periodic_notification(callback_query.from_user.id,
                                                                 product_id))
    id_list.append(product_id)
    await callback_query.message.answer(text)


async def periodic_notification(chat_id, product_id):
    while True:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Отписаться", callback_data=f"unsubscribe_{product_id}")]
        ])
        product_info_instance = WildberriesProductInfo(product_id)
        product_info = product_info_instance.fetch_product_info()
        message_text = f"<b>Название</b>: {product_info['name']}\n" \
                       f"<b>Артикул</b>: <code>{product_info['articul']}</code>\n" \
                       f"<b>Цена</b>: {.2} руб.\n" \
                       f"<b>Рейтинг</b>: {product_info['rating']} ⭐\n"
        await bot.send_message(chat_id, message_text, reply_markup=keyboard)
        await asyncio.sleep(300)


@router.callback_query(lambda cq: cq.data.startswith('unsubscribe_'))
async def handle_unsubscribe_callback(callback_query: CallbackQuery):
    product_id = callback_query.data.split('_')[1]
    if product_id in task and not task[product_id].cancelled():
        task[product_id].cancel()
        task.pop(product_id, None)
        await callback_query.message.answer(f"Вы отписались от уведомлений о товаре с ID: {product_id}")
        await callback_query.answer("Вы успешно отписались!", show_alert=False)
    else:
        await callback_query.answer("Уже отписаны или подписка не найдена.", show_alert=False)
