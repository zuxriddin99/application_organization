import asyncio
from apps.main import models as main_models
from aiogram import types
from aiogram.dispatcher import FSMContext
from django.core.exceptions import ValidationError
from apps.bot import buttons as b
from apps.bot.constants import SLEEP_TIME
from apps.bot.dispatcher import dp
from apps.bot import button_text as b_t


@dp.message_handler(lambda x: x.chat.type == 'private', commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer(
        f'Здравствуйте {message.from_user.full_name}! Я бот компании Zood. Нажмите на кнопку начать, для того что бы ознокомиться с моими возможностями 👇',
        reply_markup=b.first_b
    )


@dp.message_handler(lambda message: message.text == b_t.START)
async def ask_phone_number_welcome(message: types.Message):
    """
    This handler will be called when user sends Начать
    """
    await message.answer(
        f'{message.from_user.full_name} Please enter your phone number before use',
        reply_markup=b.ask_phone_b
    )


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_phone_number(message: types.Message):
    """
    Get user phone number and create user in our system
    """
    data = message.contact
    client, _ = await main_models.Client.objects.aget_or_create(telegram_user_id=data.user_id,
                                                                phone_number=data.phone_number)
    await message.answer(
        f'{message.from_user.full_name}, Чем я могу вам помочь?', reply_markup=await b.get_categories_list_button()
    )


async def remove_old_messages(state: FSMContext):
    async with state.proxy() as data:
        messages = data['messages']
        for mess in messages:
            await mess.delete()
