from aiogram.types import Message
import aiosqlite


class User:
    def __init__(self, message=Message):
        self.username = message.from_user.username
        self.name = message.from_user.first_name
        self.id = message.from_user.id


async def add_user_to_database(user_id, name):
    async with aiosqlite.connect('database.db') as conn:
        cur = await conn.cursor()
        await cur.execute(
            f'''CREATE TABLE IF NOT EXISTS users
                (id INT UNIQUE, name TEXT)''')
        await conn.commit()
        await cur.execute(f'INSERT OR IGNORE INTO users (id, name)'
                          f'VALUES (?, ?)', (user_id, name,))
        await conn.commit()
