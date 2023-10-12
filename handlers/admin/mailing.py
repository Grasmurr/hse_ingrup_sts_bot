from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, InlineKeyboardButton, InlineKeyboardMarkup, \
    CallbackQuery
from aiogram.dispatcher import FSMContext
import aiosqlite
from filters import IsAdmin
from loader import dp, bot
from states import MailState
from .panel import admin_panel

mess = ''


@dp.message_handler(IsAdmin(), text='Рассылка')
async def cmd_sos(message: Message):
    markup = ReplyKeyboardMarkup()
    button1 = KeyboardButton('◀️ Назад')
    markup.add(button1)
    await message.answer('Хорошо! Отправьте сообщение, которое вы собираетесь разослать пользователям:',
                         reply_markup=markup)
    await MailState.message.set()


@dp.message_handler(state=MailState, content_types=['text'])
async def message_to_mail(message: Message, state: FSMContext):
    global mess
    mess = message.text
    if mess == '◀️ Назад':
        await admin_panel(message=message)
        await state.finish()
    else:
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='Продолжить', callback_data='finish_mailing')

        markup.add(button1)

        await message.answer(f'Вы собираетесь отправить сообщение пользователям: \n\n{mess}', reply_markup=markup)


@dp.callback_query_handler(state=MailState)
async def finish_mailing(call: CallbackQuery, state: FSMContext):
    async with aiosqlite.connect('database.db') as conn:
        cur = await conn.cursor()
        await cur.execute(f'SELECT * FROM users')
        rows = [list(i)[0] for i in await cur.fetchall()]
        for i in rows:
            if i != call.message.chat.id:
                await bot.send_message(chat_id=i, text=mess)

        await bot.send_message(chat_id=call.message.chat.id, text=f'Готово! Рассылка по {len(rows)}'
                                                                  f' пользователям завершена!')
        await admin_panel(message=call.message)
        await state.finish()
