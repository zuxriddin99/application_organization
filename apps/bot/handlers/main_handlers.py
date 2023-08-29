import asyncio
import datetime
from io import BytesIO
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import CallbackQuery, ParseMode

from apps.bot.config import bot
from apps.bot.utils import get_all_categories_list, get_documents_list, return_document, read_file, check_permissions, \
    check_permission_not_decorator
from apps.main import models as main_models
from aiogram import types
from django.core.exceptions import ValidationError
from apps.bot import buttons as b
from apps.bot.dispatcher import dp
from apps.bot import button_text as b_t
from aiogram.dispatcher import FSMContext


class SickLeaveOrder(StatesGroup):
    waiting_for_date = State()


class HolidayOrder(StatesGroup):
    waiting_for_date = State()


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
async def documents_list(message: types.Message, state: FSMContext):
    if not await check_permission_not_decorator(message):
        return
    if message.text == b_t.BEST_TEAMMATE:
        employer: main_models.Employer = await main_models.Employer.objects.afirst()
        await message.answer_photo(photo=read_file_from_django(employer.image), caption=employer.initials,
                                   parse_mode=ParseMode.HTML)
    elif message.text == b_t.NEWS:
        have_news = False
        async for news in main_models.News.objects.all():
            have_news = True
            html_message = f'<b>{news.name}</b>\n{news.description}'
            if news.image:
                await message.answer_photo(photo=read_file_from_django(news.image),
                                           caption=html_message,
                                           parse_mode=ParseMode.HTML)
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
        today = datetime.date.today()
        if doc.response_msg:
            await message.answer(doc.response_msg)
        if doc.file:
            await bot.send_document(message.chat.id, read_file_from_django(doc.file))
        if message.text == b_t.SICK_LEAVE:
            print(89, '------------------')
            await message.answer("Отправить дату в этом формате(день/месяц/год)")
            await message.answer(f"{today.day}/{today.month}/{today.year}")
            await state.set_state(SickLeaveOrder.waiting_for_date.state)
        elif message.text in await get_documents_list(b_t.HOLIDAY):
            print(95, '------------------')
            await message.answer("Отправить дату в этом формате(день/месяц/год)")
            await message.answer(f"{today.day}/{today.month}/{today.year}")
            await state.set_state(HolidayOrder.waiting_for_date.state)
            await state.update_data(type_holiday=message.text)


@dp.message_handler(state=SickLeaveOrder.waiting_for_date)
async def handler_sick_leave_date(message: types.Message, state: FSMContext):
    try:
        client = await main_models.Client.objects.aget(telegram_user_id=message.from_user.id)
        date_str = message.text
        date = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
        await main_models.SickLeave.objects.acreate(client=client, date=date)
        await message.answer("Ваша дата отправил администратору")
        await state.finish()
    except ValueError:
        today = datetime.date.today()
        await message.answer("Отправить дату в этом формате(день/месяц/год)")
        await message.answer(f"{today.day}/{today.month}/{today.year}")
        await state.set_state(SickLeaveOrder.waiting_for_date.state)


@dp.message_handler(state=HolidayOrder.waiting_for_date)
async def handler_holiday_date(message: types.Message, state: FSMContext):
    try:
        client = await main_models.Client.objects.aget(telegram_user_id=message.from_user.id)
        holiday_name = await state.get_data()
        holiday = await main_models.Document.objects.aget(name=holiday_name['type_holiday'])
        date_str = message.text
        date = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
        await main_models.Holiday.objects.acreate(client=client, date=date, type_holiday=holiday)
        await message.answer("Ваша дата отправил администратору")
        await state.finish()
    except ValueError:
        today = datetime.date.today()
        await message.answer("Отправить дату в этом формате(день/месяц/год)")
        await message.answer(f"{today.day}/{today.month}/{today.year}")
        await state.set_state(HolidayOrder.waiting_for_date.state)


def read_file_from_django(file):
    file_stream = BytesIO(file.read())
    file_stream.seek(0)  # Move the stream cursor to the beginning
    return types.InputFile(file_stream, filename=file.name)
