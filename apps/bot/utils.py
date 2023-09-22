from aiogram.contrib.middlewares import logging
from aiogram.types import ParseMode, ReplyKeyboardMarkup
from django.db.models import Q
import asyncio
from aiogram import types
from django.utils import timezone

from apps.bot.config import bot
from apps.main import models as main_models
from asgiref.sync import sync_to_async
from typing import List

from conf.settings import DOMAIN


@sync_to_async
def get_admins_list() -> List[str]:
    """
    :return all admins telegram id's list
    """
    admin_telegram_ids = main_models.Client.objects.filter(is_admin=True).values_list('telegram_user_id', flat=True)
    for c in admin_telegram_ids:
        '''
            timming loop. itself set a time by the time taken for iterate over the all Client.objects.filter()
        '''
        pass
    return list(admin_telegram_ids)


@sync_to_async
def get_all_categories_list() -> List[str]:
    """
    :return all categories name list
    """
    categories = main_models.Category.objects.filter(parent=None).values_list('name', flat=True)
    for c in categories:
        '''
            timming loop. itself set a time by the time taken for iterate over the all Category.objects.all()
        '''
        pass
    return list(categories)


@sync_to_async
def get_all_categories_with_parent() -> List[str]:
    """
    :return all categories name list
    """
    categories = main_models.Category.objects.all().values_list('name', flat=True)
    for c in categories:
        '''
            timming loop. itself set a time by the time taken for iterate over the all Category.objects.all()
        '''
        pass
    return list(categories)


@sync_to_async
def get_client_old_holidays(client_id: int):
    holidays = main_models.Holiday.objects.filter(client_id=client_id, end_date__lte=timezone.now().date())
    for c in holidays:
        '''
            timming loop. itself set a time by the time taken for iterate over the all Category.objects.all()
        '''
        pass
    return holidays


@sync_to_async
def get_client_new_holidays(client_id: int):
    holidays = main_models.Holiday.objects.filter(client_id=client_id, start_date__gte=timezone.now().date())
    for c in holidays:
        '''
            timming loop. itself set a time by the time taken for iterate over the all Category.objects.all()
        '''
        pass
    return holidays


@sync_to_async
def get_categories_list(name: str, is_main=True) -> List[str]:
    """
    :return categories name list
    """
    if name == '':
        f = Q()
    else:
        f = Q(parent__name=name)
    if is_main:
        f = f & Q(parent=None)
    categories = main_models.Category.objects.filter(f).values_list('name', flat=True)
    for c in categories:
        '''
            timming loop. itself set a time by the time taken for iterate over the all Category.objects.all()
        '''
        pass
    return list(categories)


@sync_to_async
def get_documents_list(category_name: str) -> List[str]:
    """
    :return documents list
    """
    if category_name == '':
        f = Q()
    else:
        f = Q(category__name=category_name)
    documents = main_models.Document.objects.filter(f).values_list('name', flat=True)
    for c in documents:
        '''
            timming loop. itself set a time by the time taken for iterate over the all Category.objects.all()
        '''
        pass
    return list(documents)


@sync_to_async
def return_document(name: str) -> main_models.Document:
    """
    :return document
    """
    document = main_models.Document.objects.aget(name=name)
    return document


async def split_text(long_text, siz=4000) -> []:
    # Split the long text into chunks at spaces
    words = long_text.split()
    chunks = []
    current_chunk = ""
    for word in words:
        if len(current_chunk) + len(word) + 1 <= siz:  # Check if adding the word exceeds the limit
            if current_chunk:
                current_chunk += " "  # Add a space between words
            current_chunk += word
        else:
            chunks.append(current_chunk)
            current_chunk = word

    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


async def send_message_to_users(clients_id_list: List, news: main_models.News):
    html_message = f'<b>{news.name}</b>\n{news.description}'
    # texts = await split_text(html_message, 1000)
    # for text in texts:
    if news.image:
        file = await read_file(news.image.path)
        for client_id in clients_id_list:
            await bot.send_photo(chat_id=client_id, photo=file, caption=html_message, parse_mode=ParseMode.HTML)
    else:
        for client_id in clients_id_list:
            await bot.send_message(chat_id=client_id, text=html_message, parse_mode=ParseMode.HTML)


async def read_file(filename):
    try:
        loop = asyncio.get_event_loop()
        with open(filename, 'rb') as file:
            content = await loop.run_in_executor(None, file.read)
            return content
    except FileNotFoundError:
        return None


def check_permissions():
    def decorator(handler):
        async def wrapped(message: types.Message):
            empty_list = ReplyKeyboardMarkup(resize_keyboard=True)
            try:
                client = await main_models.Client.objects.aget(telegram_user_id=message.from_user.id)
                if client.is_approved:
                    await handler(message)
                else:
                    await message.answer('Админстратор ещё не одобрил вашу заявку.', reply_markup=None)
            except main_models.Client.DoesNotExist:
                await message.reply("Нажмите /start",
                                    reply_markup=empty_list)

        return wrapped

    return decorator


async def check_permission_not_decorator(message: types.Message):
    empty_list = ReplyKeyboardMarkup(resize_keyboard=True)
    try:
        client = await main_models.Client.objects.aget(telegram_user_id=message.from_user.id)
        if client.is_approved:
            return True
        else:
            await message.answer('Админстратор ещё не одобрил вашу заявку.', reply_markup=None)
            return False

    except main_models.Client.DoesNotExist:
        await message.reply("Нажмите /start",
                            reply_markup=empty_list)
        return False


async def send_message(user_id, message_text, buttons):
    try:
        await bot.send_message(user_id, message_text, reply_markup=buttons, parse_mode=ParseMode.HTML)
    except Exception as e:
        pass


async def send_notification_to_admin(text: str):
    admins_telegram_ids = await get_admins_list()
    for user_id in admins_telegram_ids:
        await send_message(user_id, text, None)


async def send_notification_to_admin_with_files(file, caption):
    admins_telegram_ids = await get_admins_list()
    for user_id in admins_telegram_ids:
        await bot.send_document(user_id, file, caption=caption)


async def generate_holiday_notification_for_admin(holiday: main_models.Holiday):
    url = f"{DOMAIN}main/client/{holiday.client.id}/change/#%D0%BE%D1%82%D0%BF%D1%83%D1%81%D0%BA-tab"
    text = f"Уведомление\n" \
           f"<a href='{url}'>ФИО:{holiday.client.full_name_from_passport}.</a>\n отправил заявление об отпуске.\n" \
           f"Тип отпуск:{holiday.type_holiday}.\n" \
           f"Дата начала {holiday.start_date}\n" \
           f"Дата окончания: {holiday.end_date}"
    await send_notification_to_admin(text)


async def generate_auth_notification_for_admin(client: main_models.Client):
    url = f"{DOMAIN}main/client/{client.id}/change/"
    text = f"Уведомление\n" \
           f"<a href='{url}'>ФИО:{client.full_name}.</a> отправил заявку на использование системы."
    await send_notification_to_admin(text)
