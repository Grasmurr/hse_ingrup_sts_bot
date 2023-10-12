from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.dispatcher import FSMContext
import aiosqlite
from filters import IsAdmin
from loader import dp, bot
from states import EditEventState
from .panel import admin_panel
from models.event import delete_events


@dp.message_handler(IsAdmin(), text='Удалить мероприятие')
async def choose_event_to_delete(mess: Message):
    async with aiosqlite.connect('database.db') as conn:
        cur = await conn.cursor()
        await cur.execute(f'SELECT * FROM events')
        events = [list(i) for i in await cur.fetchall()]
        if events:
            print(events)

            buttons = [InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[0]}') for i in events]
            markup = InlineKeyboardMarkup()
            for i in buttons:
                markup.add(i)
            markup.add(InlineKeyboardButton(text='Отмена', callback_data='Cancel'))
            await mess.answer('Хорошо! Выберите мероприятие, которое хотите удалить:', reply_markup=markup)
            await EditEventState.delete_event.set()
        else:
            await mess.answer('Кажется, еще нечего удалять')


@dp.callback_query_handler(state=EditEventState.delete_event)
async def final_deleting_stage(call: CallbackQuery, state: FSMContext):
    req = call.data
    if req == 'Cancel':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await call.message.answer('Отмена!')
        await admin_panel(message=call.message)
        await state.finish()
    else:
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='Продолжить', callback_data=f'{req}')
        button2 = InlineKeyboardButton(text='Отмена', callback_data=f'Cancel')

        markup.add(button1, button2)

        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=f'Вы точно хотите удалить мероприятие {req}?',
                                    reply_markup=markup)
        await EditEventState.final_delete.set()


@dp.callback_query_handler(state=EditEventState.final_delete)
async def delete_event_from_database(call: CallbackQuery, state: FSMContext):
    req = call.data
    if req == 'Cancel':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await call.message.answer('Отмена!')
        await admin_panel(message=call.message)
        await state.finish()
    else:
        await delete_events(name_of_event=req)
        await call.message.answer('Успешно удалено!')
        await admin_panel(message=call.message)
        await state.finish()
