from aiogram import Dispatcher
from .is_admin import IsAdmin
from .is_user import IsUser
from aiogram.dispatcher.filters import CommandStart


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsUser)
    dp.filters_factory.bind(CommandStart)
