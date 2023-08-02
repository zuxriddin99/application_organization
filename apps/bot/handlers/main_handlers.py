import asyncio
from apps.main import models as main_models
from aiogram import types
from aiogram.dispatcher import FSMContext
from django.core.exceptions import ValidationError
from apps.bot import buttons as b
from apps.bot.constants import SLEEP_TIME
from apps.bot.dispatcher import dp
from apps.bot import button_text as b_t


@dp.message_handler(lambda message: message.text == b_t.INFO)
async def ask_phone_number_welcome(message: types.Message):
    """
    return info about bot
    """
    print()
    await message.answer(
        f'Information about bot',
        reply_markup=await b.get_categories_list_button()
    )
