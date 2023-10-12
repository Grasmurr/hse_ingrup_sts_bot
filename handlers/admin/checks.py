from aiogram import executor, types, Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import text, bold
import asyncio
import aiosqlite
from filters import IsAdmin
from loader import dp