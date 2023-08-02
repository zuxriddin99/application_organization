from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from apps.bot import button_text as b_t
from apps.bot.utils import get_all_categories_list, get_documents_list

button_nachat = KeyboardButton(b_t.START)
button_ask_phone = KeyboardButton(b_t.ASK_PHONE, request_contact=True)

ask_phone_b = ReplyKeyboardMarkup(resize_keyboard=True)

ask_phone_b.add(button_ask_phone)
first_b = ReplyKeyboardMarkup(resize_keyboard=True)
first_b.add(button_nachat)


async def get_categories_list_button() -> ReplyKeyboardMarkup():
    all_categories = await get_all_categories_list()
    category_list = ReplyKeyboardMarkup(resize_keyboard=True)
    button_info = KeyboardButton(b_t.INFO, data='test')
    while all_categories:
        buttons = []
        if len(all_categories) >= 2:
            buttons.append(all_categories.pop(0))
        buttons.append(all_categories.pop(0))
        category_list.add(*buttons)
    category_list.add(button_info)
    return category_list


async def get_document_list_button(category_name: str) -> ReplyKeyboardMarkup():
    all_documents = await get_documents_list(category_name)
    documents_list = ReplyKeyboardMarkup(resize_keyboard=True)
    button_info = KeyboardButton(b_t.BACK)
    for doc_name in all_documents:
        documents_list.add(KeyboardButton(doc_name))
    documents_list.add(button_info)
    return documents_list
