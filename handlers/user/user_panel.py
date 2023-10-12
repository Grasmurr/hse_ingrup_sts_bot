from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import Message
from aiogram import Dispatcher
from loader import dp
from filters import IsUser


@dp.message_handler(text='Контакт оператора')
async def cmd_sos(message: Message):
    await message.answer('Вы можете написать нам в группу вк: https://vk.com/ingroupctc, либо в телеграм: @username')


@dp.message_handler(text='Мои билеты')
async def list_of_tickets(message: Message):
    await message.answer('Список ваших билетов:')


@dp.message_handler(text='Ближайшие мероприятия')
async def list_of_tickets(message: Message):
    await message.answer('Ближайшие мероприятия:')


@dp.message_handler(content_types=['text'])
async def wrong_text(message: Message):
    await message.answer('Кажется, на это бот не запрограммирован...')
