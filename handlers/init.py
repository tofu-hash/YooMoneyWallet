from aiogram.bot import Bot
from aiogram.utils import executor
from utils.tools import *
from aiogram.dispatcher import Dispatcher
from aiogram.types import (CallbackQuery, Message,
                           BotCommand, InlineQueryResultArticle,
                           InputTextMessageContent, InlineQuery)
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from utils.unix_time import now_unix_time, get_datetime
from utils.db_middleware import execute
from utils.keyboards import *
from utils.states import *
import logging
import config

logging.basicConfig(level=logging.INFO, filename="logs.log", filemode="w")

bot = Bot(token=config.API_KEY)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
