import asyncio

from apps.bot.utils import check_permissions
from apps.main import models as main_models
from aiogram import types
from aiogram.dispatcher import FSMContext
from django.core.exceptions import ValidationError
from apps.bot import buttons as b
from apps.bot.constants import SLEEP_TIME
from apps.bot.dispatcher import dp
from apps.bot import button_text as b_t
from aiogram.dispatcher.filters import Text


@dp.message_handler(lambda x: x.chat.type == 'private', commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer(
        f'Здравствуйте {message.from_user.full_name}! Я бот компании Zood. Нажмите на кнопку начать, чтобы ознакомиться с моими возможностями 👇',
        reply_markup=b.first_b
    )


@dp.message_handler(lambda message: message.text == b_t.START)
async def ask_full_name_welcome(message: types.Message):
    """
    This handler will be called when user sends Начать
    """
    await message.answer('Пожалуйста, введите свое ФИО перед использованием.\n')
    await message.answer('Пример 👇 ')
    await message.answer('ФИО:Мельникова Ксения Витальевна')



@dp.message_handler(Text(startswith='ФИО:'))
async def handler_full_name(message: types.Message):
    full_name = message.text.replace('ФИО:', '')
    data = message.from_user
    client, _ = await main_models.Client.objects.aget_or_create(telegram_user_id=data.id,
                                                                defaults={'full_name': full_name,
                                                                          'telegram_user_name': data.full_name})
    await message.answer(
        f'{full_name}, Чем я могу вам помочь?', reply_markup=await b.get_categories_list_button()
    )


async def remove_old_messages(state: FSMContext):
    async with state.proxy() as data:
        messages = data['messages']
        for mess in messages:
            await mess.delete()
