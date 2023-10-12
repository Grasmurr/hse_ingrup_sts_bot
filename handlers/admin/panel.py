from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from filters import IsAdmin
from loader import dp
from states import AddEventState


@dp.message_handler(IsAdmin(), commands='admin')
async def admin_panel(message: Message):
    markup = ReplyKeyboardMarkup()
    button1 = KeyboardButton('Добавить/удалить мероприятие')
    button2 = KeyboardButton('Проверить переводы')
    button3 = KeyboardButton('Рассылка')

    markup.add(button1)
    markup.add(button2, button3)

    await message.answer('Админ панель!\n\nЧтобы вернуться в панель пользователя, можно нажать на /start',
                         reply_markup=markup)


@dp.message_handler(IsAdmin(), text='Добавить/удалить мероприятие')
async def edit_event(message: Message):
    markup = ReplyKeyboardMarkup()
    button1 = KeyboardButton('Добавить мероприятие')
    button2 = KeyboardButton('Удалить мероприятие')
    button3 = KeyboardButton('◀️ Назад')

    markup.add(button1)
    markup.add(button2)
    markup.add(button3)

    await message.answer('Выберите, что вы хотите сделать:', reply_markup=markup)


@dp.message_handler(IsAdmin(), text=['◀️ Назад', 'Добавить мероприятие'])
async def continue_editing_event(message: Message):
    mess = message.text
    if mess == '◀️ Назад':
        await admin_panel(message=message)
    elif mess == 'Добавить мероприятие':
        markup = ReplyKeyboardMarkup()
        button = KeyboardButton('◀️ Назад')
        markup.add(button)
        await message.answer('Хорошо! Пожалуйста, отправьте название мероприятия: (не более 35 символов)',
                             reply_markup=markup)
        await AddEventState.name_of_event.set()
