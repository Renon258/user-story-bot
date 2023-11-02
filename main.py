import aiogram
from aiogram import Bot, Dispatcher, types, executor

from datetime import datetime

from config import TOKEN

from database import UserStoryDB

db = UserStoryDB()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

allowed_chats = []

@dp.message_handler(commands=['get_userstories'])
async def process_get(message : types.Message):
    # if message.chat.id not in allowed_chats:
    #     return

    await bot.send_message(message.chat.id, db.get_userstory())

# , chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP]
# message.chat.id in allowed_chats
@dp.message_handler(content_types=types.ContentType.TEXT)
async def process_hashtag(message : types.Message):
    if not (True and '#userstory' in message.text):
        return

    from_user = message.from_user.username
    text = message.text.replace('#userstory', '').strip().split('\n', maxsplit=2)

    if len(text) < 2:
        await message.answer('Не коректно введені дані')
        with open('logs.txt', 'a', encoding='utf-8') as file:
            file.write(str(datetime.now()) + ' user: ' + from_user + ' try to add:\n' + '\n'.join(text) + '\n\n')
        
        return
    
    db.add_userstory(from_user=from_user, title=text[0], decs=text[1])

    with open('logs.txt', 'a', encoding='utf-8') as file:
        file.write(str(datetime.now()) + ' user: ' + from_user + ' added:\n' + '\n'.join(text) + '\n\n') 

    await message.answer('Успішно додано')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)