from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from apps.bot import button_text as b_t
from apps.bot.utils import get_all_categories_list, get_documents_list, get_categories_list
from apps.main.models import Category

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


def get_categories_list_button_sync() -> ReplyKeyboardMarkup():
    all_categories = list(Category.objects.all().values_list('name', flat=True))
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
    print(category_name, '------------------------------------------------------------------------')
    all_documents = await get_documents_list(category_name)
    sub_categories = await get_categories_list(category_name, is_main=False)
    documents_list = ReplyKeyboardMarkup(resize_keyboard=True)
    button_info = KeyboardButton(b_t.BACK)
    if sub_categories:
        for sub_cat_name in sub_categories:
            documents_list.add(KeyboardButton(sub_cat_name))
    for doc_name in all_documents:
        documents_list.add(KeyboardButton(doc_name))

    documents_list.add(button_info)
    return documents_list


async def get_empty_list_button() -> ReplyKeyboardMarkup():
    empty_list = ReplyKeyboardMarkup(resize_keyboard=True)
    return empty_list


async def get_confirm_list_button(type_holiday: str) -> ReplyKeyboardMarkup():
    confirm_button = InlineKeyboardButton(text="Подтверждаю", callback_data=f"confirm_b-{type_holiday}")
    not_button = InlineKeyboardButton(
        text="Нет, передумал", callback_data=f"no_b-{type_holiday}")
    return InlineKeyboardMarkup().add(confirm_button, not_button)
