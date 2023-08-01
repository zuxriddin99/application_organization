import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from django.core.exceptions import ValidationError

from apps.bot.constants import SLEEP_TIME
from apps.bot.dispatcher import dp


@dp.message_handler(lambda x: x.chat.type == 'private', commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer(
        'Выберите тип отчета',
    )


async def remove_old_messages(state: FSMContext):
    async with state.proxy() as data:
        messages = data['messages']
        for mess in messages:
            await mess.delete()
