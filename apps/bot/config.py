import logging
import os

from aiogram import Bot

logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=os.environ.get("TELEGRAM_TOKEN", '6573821562:AAEZJ-YfPrf_pq0ET418qXVQGqYjuoymEDI'))
