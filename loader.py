from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import data.config as config


bot = Bot(token=config.token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
