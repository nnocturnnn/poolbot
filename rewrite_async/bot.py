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


@bot.message_handler(commands = ['start', 'help', 'setinfo', 'setlocate'])
def handle_start_help(message):
	if message.text.startswith('/start') == True:
		bot.send_message(message.chat.id, "Привет, чем я могу тебе помочь?", reply_markup=keyboard1)
	elif message.text == "/help":
		bot.send_message(message.chat.id, "Вот список моих команд: " 
				+ ', '.join(COMMANDS) + ". Просто напиши любую из них")
	elif message.text == '/setinfo':
		bot.send_message(message.chat.id, "А сейчас отправь инфу !")
		bot.register_next_step_handler(message, get_info)
	elif message.text == '/setlocate':
		bot.send_message(message.chat.id, "А сейчас отправь адрес !")
		bot.register_next_step_handler(message, get_locate)
	elif message.text == '/sethome':
		bot.send_message(message.chat.id, "А сейчас отправь дом инфо !")
		bot.register_next_step_handler(message, get_home)
    