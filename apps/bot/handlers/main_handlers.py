import asyncio
import datetime
from io import BytesIO
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import CallbackQuery, ParseMode

from apps.bot.config import bot
from apps.bot.utils import get_all_categories_list, get_documents_list, return_document, read_file, check_permissions, \
    check_permission_not_decorator, get_client_new_holidays, get_client_old_holidays, get_all_categories_with_parent, \
    generate_holiday_notification_for_admin, split_text
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
async def info_about_client(message: types.Message):
    """
    return info about user
    """
    client = await main_models.Client.objects.aget(telegram_user_id=message.from_user.id)

    data = f"ФИО по паспорту: {client.full_name_from_passport}\n" \
           f"Серия паспорта: {client.passport_seria}\n" \
           f"Дата приёма: {client.date_of_receipt}\n" \
           f"Должность: {client.job_title}\n" \
           f"Департамент: {client.department}"
    await message.answer(
        data,
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
    try:
        doc: main_models.Document = await main_models.Document.objects.aget(name=message.text)
        if doc.response_msg:
            await message.answer(doc.response_msg)
        if doc.file:
            await bot.send_document(message.chat.id, read_file_from_django(doc.file))
    except Exception:
        pass
    if message.text == b_t.BEST_TEAMMATE:
        async for employer in main_models.Employer.objects.all():
            await message.answer_photo(photo=read_file_from_django(employer.image), caption=employer.initials,
                                       parse_mode=ParseMode.HTML)
    elif message.text == b_t.NUMBER_OF_UNUSED_HOLIDAYS:
        client = await main_models.Client.objects.aget(telegram_user_id=message.from_user.id)
        if client.holiday_quantity not in ['', None]:
            await message.answer(
                client.holiday_quantity,
            )

    elif message.text == b_t.MY_PREVIOUS_HOLIDAYS:
        client = await main_models.Client.objects.aget(telegram_user_id=message.from_user.id)
        for i in await get_client_old_holidays(client.id):
            await message.answer(f"Тип: {i.type_holiday}\nДата начала {i.start_date}\nДата окончания: {i.end_date}")
    elif message.text == b_t.SCHEDULED_DATES:
        client = await main_models.Client.objects.aget(telegram_user_id=message.from_user.id)
        for i in await get_client_new_holidays(client.id):
            await message.answer(f"Тип: {i.type_holiday}\nДата начала {i.start_date}\nДата окончания: {i.end_date}")

    elif message.text == b_t.NEWS:
        have_news = False
        async for news in main_models.News.objects.all():
            have_news = True
            html_message = f'<b>{news.name}</b>\n{news.description}'
            # texts = await split_text(html_message, 1024)
            # print(len(texts))
            # for text in texts:

            try:
                if news.image:
                    await message.answer_photo(photo=read_file_from_django(news.image),
                                               caption=html_message,
                                               parse_mode=ParseMode.HTML)
                else:
                    await message.answer(text=html_message, parse_mode=ParseMode.HTML)
            except:
                await message.answer(text=html_message, parse_mode=ParseMode.HTML)
        if not have_news:
            await message.answer(text="no news", parse_mode=ParseMode.HTML)

    elif message.text in [b_t.TAKE_ANNUAL_LEAVE]:
        await message.answer("Отправьте дату начала отпуска и дату окончания.\n"
                             "Отправить дату в этом формате(день/месяц/год - день/месяц/год).\n"
                             "Пример: 20/8/2023 - 20/9/2023", reply_markup=await b.get_cancel_button())
        await state.set_state(HolidayOrder.waiting_for_date.state)
        await state.update_data(type_holiday=b_t.ANNUAL_LEAVE)
    elif message.text in await get_all_categories_with_parent():
        """ return documents selected category"""
        await message.answer(
            message.text,
            reply_markup=await b.get_document_list_button(message.text)
        )

    elif message.text in await get_documents_list(''):
        """ return selected document"""
        # doc: main_models.Document = await main_models.Document.objects.aget(name=message.text)
        # if doc.response_msg:
        #     await message.answer(doc.response_msg)
        # if doc.file:
        #     await bot.send_document(message.chat.id, read_file_from_django(doc.file))
        if message.text in [b_t.SICK_LEAVE, b_t.PREGNANCY_LEAVE]:
            if message.text == b_t.SICK_LEAVE:
                await message.answer("Отправьте дату начала больничный по болезни и дату окончания.\n"
                                     "Отправить дату в этом формате(день/месяц/год - день/месяц/год).\n"
                                     "Пример: 20/8/2023 - 20/9/2023", reply_markup=await b.get_cancel_button())
            else:
                await message.answer("Отправьте дату начала больничного по беременности и родам и дату окончания.\n"
                                     "Отправить дату в этом формате(день/месяц/год - день/месяц/год).\n"
                                     "Пример: 20/8/2023 - 20/9/2023", reply_markup=await b.get_cancel_button())
            await state.set_state(SickLeaveOrder.waiting_for_date.state)
            await state.update_data(type_leave=message.text)

        elif message.text in [b_t.LEAVE_WITHOUT_PAY, b_t.HOLIDAY_CARE_FOR_CHILD]:
            await message.answer("Отправьте дату начала отпуска и дату окончания.\n"
                                 "Отправить дату в этом формате(день/месяц/год - день/месяц/год).\n"
                                 "Пример: 20/8/2023 - 20/9/2023", reply_markup=await b.get_cancel_button())
            await state.set_state(HolidayOrder.waiting_for_date.state)
            await state.update_data(type_holiday=message.text)


@dp.message_handler(state=SickLeaveOrder.waiting_for_date)
async def handler_sick_leave_date(message: types.Message, state: FSMContext):
    if message.text == b_t.CANCEL:
        await message.answer('Отмена', reply_markup=await b.get_document_list_button(b_t.SICK))
        await state.finish()
        return
    type_leave = await state.get_data()
    type_leave = type_leave['type_leave']
    try:
        client = await main_models.Client.objects.aget(telegram_user_id=message.from_user.id)

        date_str = message.text.replace(' ', '').split('-')
        start_date, end_date = datetime.datetime.strptime(date_str[0], "%d/%m/%Y").date(), datetime.datetime.strptime(
            date_str[1], "%d/%m/%Y").date()
        await main_models.SickLeave.objects.acreate(client=client, start_date=start_date, end_date=end_date,
                                                    type_sick=type_leave)
        await message.answer("Указанные вами даты отправлены администратору",
                             reply_markup=await b.get_document_list_button(b_t.SICK))
        await state.finish()
    except ValueError:
        if type_leave == b_t.SICK_LEAVE:
            await message.answer(
                "Отправьте дату начала больничный по болезни и дату окончания.\n"
                "Отправить дату в этом формате(день/месяц/год - день/месяц/год).\n"
                "Пример: 20/8/2023 - 20/9/2023", reply_markup=await b.get_cancel_button())
        else:
            await message.answer(
                "Отправьте дату начала больничного по беременности и родам и дату окончания.\n"
                "Отправить дату в этом формате(день/месяц/год - день/месяц/год).\n"
                "Пример: 20/8/2023 - 20/9/2023", reply_markup=await b.get_cancel_button())
        await state.set_state(SickLeaveOrder.waiting_for_date.state)


@dp.message_handler(state=HolidayOrder.waiting_for_date)
async def handler_holiday_date(message: types.Message, state: FSMContext):
    if message.text == b_t.CANCEL:
        holiday = await state.get_data()
        holiday_type = holiday['type_holiday']
        if holiday_type == b_t.ANNUAL_LEAVE:
            reply_markup = await b.get_document_list_button(holiday_type)
        else:
            reply_markup = await b.get_document_list_button(b_t.HOLIDAY)
        await message.answer('Отмена', reply_markup=reply_markup)
        await state.finish()
        return

    try:
        holiday_name = await state.get_data()
        holiday_name = holiday_name['type_holiday']
        date_str = message.text.replace(' ', '').split('-')
        start_date, end_date = datetime.datetime.strptime(date_str[0], "%d/%m/%Y").date(), datetime.datetime.strptime(
            date_str[1], "%d/%m/%Y").date()
        after_2_weeks = datetime.date.today() + datetime.timedelta(days=14)
        if start_date < after_2_weeks:
            await message.answer(
                "Чтобы подать заявление на отпуск, вы должны уведомить об этом как минимум за 2 недели.")
            await state.set_state(HolidayOrder.waiting_for_date.state)
            return None
        else:
            await state.finish()
            await message.reply("Вы подтверждаете дату?",
                                reply_markup=await b.get_confirm_list_button(holiday_name))

            return None
            # holiday_obj = await main_models.Holiday.objects.acreate(client=client, start_date=start_date,
            #                                                         end_date=end_date,
            #                                                         type_holiday=holiday_name)
            # await generate_holiday_notification_for_admin(holiday_obj)
            #
            # await message.answer("Указанные вами даты отправлены администратору")
            # await state.finish()
    except Exception as error:
        await message.answer("Отправьте дату начала отпуска и дату окончания.\n"
                             "Отправить дату в этом формате(день/месяц/год - день/месяц/год).\n"
                             "Пример: 20/8/2023 - 20/9/2023", reply_markup=await b.get_cancel_button())
        await state.set_state(HolidayOrder.waiting_for_date.state)


# @dp.callback_query_handler(lambda query: query.data in ["confirm_b", "no_b"])
@dp.callback_query_handler()
async def check_button(call: types.CallbackQuery, state: FSMContext):
    start_date, end_date = call.message.reply_to_message.text.replace(' ', '').split('-')
    confirm, holiday = call.data.split('-')[0], call.data.split('-')[-1]
    if holiday == b_t.ANNUAL_LEAVE:
        reply_markup = await b.get_document_list_button(holiday)
    else:
        reply_markup = await b.get_document_list_button(b_t.HOLIDAY)
    if confirm == "confirm_b":
        client = await main_models.Client.objects.aget(telegram_user_id=call.message.reply_to_message.from_user.id)
        # await main_models.Holiday.objects.acreate(client=client, start_date=start_date, end_date=end_date,
        #                                           type_holiday=holiday)
        start_date, end_date = datetime.datetime.strptime(start_date, "%d/%m/%Y").date(), datetime.datetime.strptime(
            end_date, "%d/%m/%Y").date()
        holiday_obj = await main_models.Holiday.objects.acreate(client=client, start_date=start_date, end_date=end_date,
                                                                type_holiday=holiday)
        await generate_holiday_notification_for_admin(holiday_obj)
        await call.message.answer("Указанные вами даты отправлены администратору",
                                  reply_markup=reply_markup)
        await state.finish()
    if confirm == "no_b":
        await call.message.answer("Хорошо", reply_markup=reply_markup)
    # Notify the Telegram server that the callback query is answered successfully
    await call.answer()
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        reply_markup=None)


def read_file_from_django(file):
    file_stream = BytesIO(file.read())
    file_stream.seek(0)  # Move the stream cursor to the beginning
    return types.InputFile(file_stream, filename=file.name)
