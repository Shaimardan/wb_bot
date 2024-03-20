from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kb

admin = Router()


class Newsletter(StatesGroup):
    message = State()


class AdminProtect(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in [5791374868]


@admin.message(AdminProtect(), Command('apanel'))
async def apanel(message: Message):
    await message.answer('Возможные команды: /newsletter\n/add_item')


@admin.message(AdminProtect(), Command('newsletter'))
async def newsletter(message: Message, state: FSMContext):
    await state.set_state(Newsletter.message)
    await message.answer('Отправьте сообщение, которое вы хотите разослать всем пользователям')
