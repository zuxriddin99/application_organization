import asyncio
import logging

from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.bot.utils import send_message_to_user
from apps.main.models import News, Client


@receiver(post_save, sender=News)
def my_signal_receiver(sender, instance: News, created, **kwargs):
    if created:
        list(Client.objects.all().values_list('telegram_user_id', flat=True))
        asyncio.run(send_message_to_user(list(Client.objects.all().values_list('telegram_user_id', flat=True)), instance))
