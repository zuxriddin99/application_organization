from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from apps.bot.config import bot

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)
from apps.bot.handlers.start_handlers import *  # noqa
from apps.bot.handlers.main_handlers import *  # noqa
