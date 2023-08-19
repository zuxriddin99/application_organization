import asyncio
import logging

from aiogram.types import ReplyKeyboardMarkup

from apps.bot import buttons as b

from django.db.models import signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.bot.button_text import SICK_LEAVE
from apps.bot.config import bot
from apps.bot.utils import send_message_to_users, send_message
from apps.main.models import News, Client, Document


@receiver(post_save, sender=News)
def my_signal_receiver(sender, instance: News, created, **kwargs):
    if created:
        list(Client.objects.all().values_list('telegram_user_id', flat=True))
        asyncio.run(
            send_message_to_users(list(Client.objects.all().values_list('telegram_user_id', flat=True)), instance))


@receiver(post_save, sender=Client)
def client_signal_receiver(sender, instance: Client, created, **kwargs):
    if created:
        pass
    else:
        if instance.is_approved:
            asyncio.run(send_message(instance.telegram_user_id,
                                     "Администратор одобрил ваш запрос, вы можете пользоваться услугами бота.",
                                     b.get_categories_list_button_sync()))
        else:
            asyncio.run(send_message(instance.telegram_user_id,
                                     "Ваш запрос был отправлен админстратору, ожидайте подтверждения запроса.",
                                     None))


@receiver(pre_save, sender=Document)
def doc_signal_receiver(sender, instance: Document, **kwargs):
    if instance.id == 10:
        instance.name = SICK_LEAVE
