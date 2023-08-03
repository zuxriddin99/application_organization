from django.core.management import BaseCommand
from aiogram.utils import executor

from apps.bot.dispatcher import dp


class Command(BaseCommand):
    def handle(self, *args, **options):
        executor.start_polling(dp, skip_updates=False)
