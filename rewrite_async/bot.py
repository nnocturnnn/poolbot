import logging
import banking
import db

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '1054227476:AAHMD3T4QOhQnJ1oBfLYaYI64Rx8O4dKWX8'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")
    