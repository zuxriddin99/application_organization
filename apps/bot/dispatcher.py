import logging

from aiogram import Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from apps.bot.config import bot

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)


# Custom decorator to check user permissions

from apps.bot.handlers.start_handlers import *  # noqa
from apps.bot.handlers.main_handlers import *  # noqa
