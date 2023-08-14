import asyncio
from random import randint
from typing import List

from aiogram.types import CallbackQuery, ParseMode
from asgiref.sync import sync_to_async

from apps.bot.config import bot
from apps.bot.utils import get_all_categories_list, get_documents_list, return_document, read_file, check_permissions
from apps.main import models as main_models
from aiogram import types
from aiogram.dispatcher import FSMContext
from django.core.exceptions import ValidationError
from apps.bot import buttons as b
from apps.bot.dispatcher import dp
from apps.bot import button_text as b_t


@dp.message_handler(lambda message: message.text == b_t.INFO)
@check_permissions()
async def info_about_bot(message: types.Message):
    """
    return info about bot
    """

    await message.answer(
        f'Information about bot',
        reply_markup=await b.get_categories_list_button()
    )


@dp.message_handler(lambda message: message.text == b_t.BACK)
@check_permissions()
async def back_to_category_list(message: types.Message):
    """
    return info about bot
    """
    await message.answer(
        f'{message.from_user.full_name}, Чем я могу вам помочь?',
        reply_markup=await b.get_categories_list_button()
    )


@dp.message_handler()
@check_permissions()
async def documents_list(message: types.Message):
    if message.text == b_t.BEST_TEAMMATE:
        employer = await main_models.Employer.objects.afirst()
        file = await read_file(employer.image.path)
        await message.answer_photo(photo=file, caption=employer.initials, parse_mode=ParseMode.HTML)
    elif message.text == b_t.NEWS:
        have_news = False
        async for news in main_models.News.objects.all():
            have_news = True
            html_message = f'<b>{news.name}</b>\n{news.description}'
            if news.image:
                file = await read_file(news.image.path)
                await message.answer_photo(photo=file, caption=html_message, parse_mode=ParseMode.HTML)
            else:
                await message.answer(text=html_message, parse_mode=ParseMode.HTML)
        if not have_news:
            await message.answer(text="no news", parse_mode=ParseMode.HTML)
    elif message.text in await get_all_categories_list():
        """ return documents selected category"""
        await message.answer(
            message.text,
            reply_markup=await b.get_document_list_button(message.text)
        )


    elif message.text in await get_documents_list(''):
        """ return selected document"""
        doc: main_models.Document = await main_models.Document.objects.aget(name=message.text)
        if doc.response_msg:
            await message.answer(doc.response_msg)
        with open(doc.file.path, 'rb') as file:
            # Use `send_document()` to send the file to the user
            await bot.send_document(message.chat.id, file)
