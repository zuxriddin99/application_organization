import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from asgiref.sync import sync_to_async

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


class OrderFullName(StatesGroup):
    waiting_for_full_name = State()


@dp.message_handler(lambda x: x.chat.type == 'private', commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer(
        f'Здравствуйте {message.from_user.full_name}! Я бот компании Zood. Нажмите на кнопку начать, чтобы ознакомиться с моими возможностями 👇',
        reply_markup=b.first_b
    )


@dp.message_handler(lambda message: message.text == b_t.START, state="*")
async def ask_full_name_welcome(message: types.Message, state: FSMContext):
    """
    This handler will be called when user sends Начать
    """
    try:
        client = await main_models.Client.objects.aget(telegram_user_id=message.from_user.id)
        if client.is_approved:
            await message.answer(
                f'{message.from_user.full_name}, Чем я могу вам помочь?',
                reply_markup=await b.get_categories_list_button()
            )
        else:
            await message.answer('Ваша информация отправлена администратору, подождите',
                                 reply_markup=types.ReplyKeyboardRemove)

    except main_models.Client.DoesNotExist:
        await message.answer('Пожалуйста, введите свое ФИО перед использованием.\n', reply_markup=types.ReplyKeyboardRemove)
        await state.set_state(OrderFullName.waiting_for_full_name.state)


@dp.message_handler(state=OrderFullName.waiting_for_full_name)
async def handler_full_name(message: types.Message, state: FSMContext):
    full_name = message.text
    data = message.from_user
    client, created = await main_models.Client.objects.aget_or_create(telegram_user_id=data.id,
                                                                      defaults={'full_name': full_name,
                                                                                'telegram_user_name': data.full_name})
    if not created and full_name != client.full_name:
        async_update_client_full_name = sync_to_async(sync_update_client_full_name)
        await async_update_client_full_name(client, full_name)

    # await message.answer(
    #     f'{full_name}, Чем я могу вам помочь?', reply_markup=await b.get_categories_list_button()
    # )
    await message.answer(
        "Администрация одобряет вас, после чего вы можете использовать бота"
    )
    await state.finish()


async def remove_old_messages(state: FSMContext):
    async with state.proxy() as data:
        messages = data['messages']
        for mess in messages:
            await mess.delete()


def sync_update_client_full_name(client, full_name):
    client.full_name = full_name
    client.save(update_fields=['full_name'])
