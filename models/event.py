from aiogram.types import Message
import aiosqlite


class Event:
    def __init__(self, name, cost, desc, photo_path):
        self.name = name
        self.cost = cost
        self.desc = desc
        self.photo_path = photo_path


async def add_event(name, cost, desc, photo_path):
    async with aiosqlite.connect('database.db') as conn:
        cur = await conn.cursor()
        await cur.execute(
            f'''CREATE TABLE IF NOT EXISTS events
                (name TEXT, cost TEXT, desc TEXT, photo_path TEXT)''')
        await conn.commit()
        await cur.execute(f'INSERT INTO events (name, cost, desc, photo_path)'
                          f'VALUES (?, ?, ?, ?)', (name, str(cost), desc, photo_path,))
        await conn.commit()


async def get_events():
    async with aiosqlite.connect('database.db') as conn:
        cur = await conn.cursor()
        await cur.execute(f'SELECT * FROM users')
        rows = [list(i)[0] for i in await cur.fetchall()]
        print(rows)


async def delete_events(name_of_event):
    async with aiosqlite.connect('database.db') as conn:
        cur = await conn.cursor()
        await cur.execute('DELETE FROM events WHERE name = ?', (name_of_event,))
        await conn.commit()

