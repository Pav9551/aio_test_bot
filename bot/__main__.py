from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
from random import shuffle
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
BOT_TOKEN = '6339702140:AAFOlVJGHgHkRZVAwb8dqOYLAe_i_5HbKPQ'

ANSWERS = [
    'Думаю, да!',
    'Не стоит.',
    'Я сомневаюсь в этом',
    'Вероятно, да',
    'Бесспорно',
    'Не могу сказать',
    'Не сейчас',
    'Спросите позже',
    'Решительно, да!'
]


host = '188.120.249.155'
port = 5432
dbname = 'email'
user = 'email'
password = 'password'


def from_base():
  #conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
  #cur = conn.cursor()
  #cur.execute(f"SELECT username FROM public.users")
  #fetch = cur.fetchall()
  #conn.close()
  #dict_room = {roomnames[room]: {'loud':fetch[0][0],'count':fetch[1][0],'percent':percent}}
  fetch = 'ничего нет'
  try:
      # Подключение к существующей базе данных
      connection = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
      connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
      # Курсор для выполнения операций с базой данных
      cursor = connection.cursor()
      sql_database = 'SELECT username FROM public.users'
      cursor.execute(sql_database)
      fetch = cursor.fetchall()

      print("Соединение с PostgreSQL открыто")
  except (Exception, Error) as error:
      print("Ошибка при работе с PostgreSQL", error)
  finally:
      if connection:
          cursor.close()
          connection.close()
          print("Соединение с PostgreSQL закрыто")
  return fetch

router: Router = Router()

@router.message(Command(commands=['start']))
async def start_command(message: Message):
    await message.answer('Привет! Я сейчас делаю синхронный запрос в базу данных...')

    answer_db = from_base()
    #answer_db = "no"
    print(len(answer_db))
    if len(answer_db) > 0:
        for user in answer_db:
            await message.answer(f"{user[0]}")
    else:
        await message.answer(f"Ничего не найдено")
@router.message(F.text.endswith('?'))
async def answer_to_questions(message: Message):
    shuffle(ANSWERS)
    await message.answer(ANSWERS[0])
@router.message()
async def answer(message: Message):
    await message.answer('Не понимаю о чем ты... Просто задай вопрос.')


async def start():
    bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()
    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':

    asyncio.run(start())
