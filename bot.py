from aiogram import executor, Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import handlers
import handlers.admin.panel
import filters
from loader import dp, bot
from models.user import User, add_user_to_database

filters.setup(dp)

@dp.message_handler(commands='start')
async def start_command(message: Message):
    user = User(message)
    markup = ReplyKeyboardMarkup()
    button1 = KeyboardButton('Ближайшие мероприятия')
    button2 = KeyboardButton('Контакт оператора')
    button3 = KeyboardButton('Мои билеты')

    markup.add(button1)
    markup.add(button3, button2)

    await message.answer_photo(photo=open('data/assets/xmysqvNvryM.jpg', 'rb'),
                               caption=f'Привет, {user.name}! Это телеграм-бот от Ингруп СТС! '
                                       f'Через него вы можете зарегистрироваться/взять билет'
                                       f' на ближайшее мероприятие! ', reply_markup=markup)
    await add_user_to_database(user_id=user.id, name=user.name)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
