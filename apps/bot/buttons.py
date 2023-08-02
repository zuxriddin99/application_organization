from aiogram import types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from apps.bot import button_text as b_t
from apps.main import models as main_models
from asgiref.sync import sync_to_async

button_nachat = KeyboardButton(b_t.START)
button_ask_phone = KeyboardButton(b_t.ASK_PHONE, request_contact=True)

ask_phone_b = ReplyKeyboardMarkup(resize_keyboard=True)

ask_phone_b.add(button_ask_phone)
first_b = ReplyKeyboardMarkup(resize_keyboard=True)
first_b.add(button_nachat)


@sync_to_async
def get_all_categories():
    categories = main_models.Category.objects.all()
    for c in categories:
        '''
            timming loop. itself set a time by the time taken for iterate over the all Category.objects.all()
        '''
        pass
    return categories


async def get_categories_list_button():
    all_categories = await get_all_categories()
    category_list = ReplyKeyboardMarkup(resize_keyboard=True)
    button_info = KeyboardButton(b_t.INFO)
    for category in all_categories:
        category_list.add(KeyboardButton(category.name))
    category_list.add(button_info)
    return category_list
