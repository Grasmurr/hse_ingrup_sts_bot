from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, ReplyKeyboardRemove,\
    InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
import requests
from loader import dp, bot
from data.config import token
from states import AddEventState
from .panel import admin_panel
from models.event import Event, add_event

name_of_event = ''


@dp.message_handler(state=AddEventState.name_of_event, content_types=['text'])
async def add_event(message: Message, state: FSMContext):
    if message.text == '◀️ Назад':
        await state.finish()
        await admin_panel(message=message)
    else:
        if len(message.text) < 35:
            global name_of_event
            name_of_event = message.text
            markup = ReplyKeyboardMarkup()
            button1 = KeyboardButton('Платное')
            button2 = KeyboardButton('Бесплатное')
            markup.add(button1, button2)
            await message.answer(f'Хорошо! Теперь выберите, будет ли {name_of_event} платным(ой)?', reply_markup=markup)
            await AddEventState.cost_of_event.set()
        else:
            await message.answer('Ошибка! название мероприятия слишком длинное! '
                                 'Постарайтесь сократить его до 35 символов...')


@dp.message_handler(state=AddEventState.cost_of_event, text=['Бесплатное', 'Платное'])
async def cost_of_the_event(message: Message):
    if message.text == 'Бесплатное':
        await message.answer(f'Хорошо! В таком случае пришлите описание {name_of_event}:',
                             reply_markup=ReplyKeyboardRemove())
        await AddEventState.description_of_event.set()
    elif message.text == 'Платное':
        await message.answer(f'Хорошо! Тогда отправьте стоимость {name_of_event} цифрой. Например: 350')

cost_of_event = 'Бесплатное'


@dp.message_handler(state=AddEventState.cost_of_event, content_types=['text'])
async def cost_of_the_event(message: Message):
    global cost_of_event
    if message.text.isdigit():
        cost_of_event = int(message.text)
        await message.answer(f'Хорошо, стоимость {name_of_event} будет: {int(message.text)}руб.\n\n'
                             f'Далее, пришлите описание мероприятия:', reply_markup=ReplyKeyboardRemove())
        await AddEventState.description_of_event.set()
    else:
        await message.answer('Кажется, вы ввели что-то неправильно, попробуйте снова...')

description_of_the_event = ''


@dp.message_handler(state=AddEventState.description_of_event, content_types=['text'])
async def desc(message: Message):
    global description_of_the_event
    description_of_the_event = message.text

    await message.answer(f'Хорошо! Напоследок, нужна еще фотография для мероприятия. '
                         f'Пожалуйста, отправьте именно фото, не файл')
    await AddEventState.event_photo.set()

photo_path = ''


@dp.message_handler(state=AddEventState.event_photo, content_types=[ContentType.PHOTO, ContentType.ANY])
async def photo(message: Message):
    global photo_path
    global cost_of_event
    if message.content_type == ContentType.PHOTO:
        # Save the photo to disk
        photo_id = message.photo[-1].file_id
        file = await bot.get_file(photo_id)
        print(file)
        response = requests.get(f"https://api.telegram.org/file/bot{token}/{file.file_path}")
        with open(f"data/assets/{file.file_id}.jpg", "wb") as f:
            photo_path = f"data/assets/{file.file_id}.jpg"
            f.write(response.content)
        await message.answer('Замечательно! Итак, мероприятие будет выглядеть следующим образом:')
        markup = InlineKeyboardMarkup()

        button1 = InlineKeyboardButton(text='Продолжить', callback_data='finish_adding_event')
        button2 = InlineKeyboardButton(text='Отмена', callback_data='Cancel')

        markup.add(button1, button2)
        if cost_of_event != 'Бесплатное':
            cost_of_event = str(cost_of_event) + ' руб.'

        await message.answer_photo(photo=open(f'{photo_path}', 'rb'),
                                   caption=f'{name_of_event}\n\nЦена: {cost_of_event}\n\n'
                                           f'Описание: {description_of_the_event}', reply_markup=markup)

        await AddEventState.finish_adding.set()
    else:
        # Handle any other type of message
        await message.answer('Пожалуйста, отправьте фото, а не файл...')


@dp.callback_query_handler(state=AddEventState.finish_adding)
async def photo(call: CallbackQuery, state: FSMContext):
    req = call.data
    if req == 'Cancel':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await call.message.answer('Отмена!')
        await admin_panel(message=call.message)
        await state.finish()
    elif req == 'finish_adding_event':
        event = Event(name=name_of_event, cost=cost_of_event, desc=description_of_the_event, photo_path=photo_path)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await call.message.answer('Мероприятие успешно добавлено!')
        await admin_panel(message=call.message)
        await state.finish()
        await add_event(name=event.name, cost=event.cost, desc=event.desc, photo_path=event.photo_path)
