import logging
import banking
import other
import db
import key as kb
import os
from geopy.geocoders import Nominatim
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


class Test(StatesGroup):
	info = State()
	locale = State()
	date = State()
	price = State()
	cardinfo = State()

API_TOKEN = '1054227476:AAG-kDMgrPFJAhfU1jT0CCJl8eLiSpIW3RI'        # TODO убрать в проде
SPOTIFY_TOKEN = '0f6f810bd15b4caeb003ec37402d0e5b'
logging.basicConfig(level=logging.INFO)
geolocator = Nominatim(user_agent="tusabot")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot,storage=MemoryStorage())



@dp.message_handler(state=Test.info)
async def info_state(message: types.Message, state: FSMContext):
	answer = message.text
	await bot.unpin_all_chat_messages(message.chat.id)
	await bot.pin_chat_message(message.chat.id, message.message_id)
	db.insert_db(message.chat.id,info=answer)
	await state.finish()

@dp.message_handler(state=Test.locale)
async def locale_state(message: types.Message, state: FSMContext):
	answer = message.text
	db.insert_db(message.chat.id,locale=answer.lower())
	await state.finish()

@dp.message_handler(state=Test.date)
async def date_state(message: types.Message, state: FSMContext):
	answer = message.text
	db.insert_db(message.chat.id,date=answer.lower())
	print(message.chat.id)
	await state.finish()

@dp.message_handler(state=Test.price)
async def price_state(message: types.Message, state: FSMContext):
	answer = message.text
	db.insert_db(message.chat.id,price=answer.lower())
	await state.finish()

@dp.message_handler(state=Test.cardinfo)
async def cardinfo_state(message: types.Message, state: FSMContext):
	answer = message.text
	db.insert_db(message.chat.id,card_info=answer.lower())
	await state.finish()







@dp.message_handler(commands=['start', 'help', 'setinfo', 'setlocale', 
							  'setdate', 'setprice','setcardinfo'])
async def send_command(message: types.Message):
	if message.text.lower() == '/start':
		db.insert_db(message.chat.id)
		await message.answer( f'{message.from_user.first_name} , добро \
		пожаловать к PartyBot!\n Есть вопросы? Обратись к помощи /help\n')
	elif message.text.lower() == "/help":
		await message.answer("Этот бот поможет организовать тусовочку\n\
/setinfo - установить информацию тусовочки\n/setlocale - установить место\n\
/setdate - установить дату\n/setprice - установить цену\n/setcardinfo \
		- установить автопроверку платежей (Monobank, PrivatBank)")
	elif message.text.lower() == "/setinfo":
		await message.answer("А теперь отправь информацию о тусовочке!")
		await Test.info.set()
	elif message.text.lower() == "/setlocale":
		await message.answer("А теперь выбери формат адреса",reply_markup=kb.inline_kb_variant_addres)
	elif message.text.lower() == "/setdate":
		await message.answer("А теперь отправь дату тусовочки!\nНапример 17.03")
		await Test.date.set()
	elif message.text.lower() == "/setprice":
		await message.answer("А теперь отправь стоимость проходки на тусовочку!")
		await Test.price.set()
	elif message.text.lower() == "/setcardinfo":
		await message.answer("А теперь выбери свой банк!",reply_markup=kb.bank_kb)
		await Test.cardinfo.set()


@dp.message_handler(content_types = ['text'])
async def send_text(message: types.Message):
	proxyDict = {
		"http"  : os.environ.get('FIXIE_URL', ''), 
		"https" : os.environ.get('FIXIE_URL', '')}
	if message.text.lower() == 'погодка':
		await message.answer(other.pogodka())
	if message.text.lower() == 'когда туса?':
		await message.answer(db.get_from_db(str(message.chat.id),"date"))
	elif message.text.lower() == 'информация':
		await message.answer(db.get_from_db(str(message.chat.id),"info"))
	elif message.text.lower() == 'кто будет?':
		await message.answer(db.get_from_db("list_user"))
	elif message.text.lower() == 'кто скинул?':
		await message.answer(db.get_from_db("list_user2"))
	elif message.text.lower() == 'геолока':
		locale = db.get_from_db(str(message.chat.id),"locale").strip()
		if locale[0].isdigit():
			await message.answer_location(locale.split()[0],locale.split()[1])
		else:
			try:
				location = geolocator.geocode(locale, language='ru')
				await message.answer(location)
				await message.answer_location(location.latitude, location.longitude)
			except:
				bot.send_message(message.chat.id, 'Cервер выебываеться попробуйте позже 😔 😔 😔')
	elif message.text.lower() == 'бюджет': #TODO исправить два трая на один
		try:
			await message.answer("Бюджет тусовочки 💴 💴 💴 " + \
				 privat_bank(os.getenv('API_PRIVAT'), proxyDict, "153753",\
				 "5168745302334229") + " гривен")
		except:
			try:
				await message.answer("Бюджет тусовочки 💴 💴 💴 " + \
					 privat_bank(os.getenv('API_PRIVAT2'),proxyDict, "155325",\
					 "5168745302334229") + " гривен")
			except:
				await message.answer('Cервер выебываеться попробуйте позже 😔 😔 😔')
	elif message.text.lower() == 'оплатить':
		await message.answer("Выберите способ оплаты :",reply_markup=kb.payment_kb)
	elif message.text.lower() == 'добавить песню в плейлист':
		await message.answer("Теперь отправьте название песни:")
	elif message.text.lower() == 'ip':
		rer = requests.get('https://ramziv.com/ip', proxies=proxyDict).text
		await message.answer(rer)
	elif message.text.lower() == 'playmusic':
		pass


@dp.callback_query_handler(lambda c: c.data == 'btn1')
async def process_callback_button1(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(callback_query.message.chat.id, 'Вы выбрали координаты\
, теперь отправьте lontitude latitude\nНапример 50.32434 47.32443')
		await Test.locale.set()

@dp.callback_query_handler(lambda c: c.data == 'btn2')
async def process_callback_button2(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(callback_query.message.chat.id, 'Вы выбрали адрес\
, теперь отправьте адрес\nНапример Киев Хрещатик 4')
		await Test.locale.set()

@dp.callback_query_handler(lambda c: c.data == 'monokey')
async def process_callback_mono(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(callback_query.from_user.id, 'Вы выбрали Монобанк \
		, теперь отправьте токен монобанка\nНапример Adf42sdf2342442sdf2314432\n\
		Чтобы получить токен монобанка перейдите по ссылке https://api.monobank.ua/')

@dp.callback_query_handler(lambda c: c.data == 'privatekey')
async def process_callback_private(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(callback_query.from_user.id, 'Вы выбрали Приватбанк \
		, теперь отправьте токен, номер карты \nНапример Adf42sdf2342442sdf2314432 4441114446179218 \n \
		Чтобы получить токен приватбанка перейдите по ссылке https://api.privatbank.ua/#p24/registration')


@dp.callback_query_handler(lambda c: c.data == 'private_pay')
async def process_callback_private_pay(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(callback_query.from_user.id, f'Вы выбрали Приватбанк \
		, теперь отправьте {1} гривен на {1} подождите после отправки 1 минуту и нажмите Проверить')

@dp.callback_query_handler(lambda c: c.data == 'mono_pay')
async def process_callback_private_pay(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(callback_query.from_user.id, f'Вы выбрали Монобанк \
		, теперь отправьте {1} гривен на {1} подождите после отправки 1 минуту и нажмите Проверить')

@dp.callback_query_handler(lambda c: c.data == 'nal_pay')
async def process_callback_private_pay(callback_query: types.CallbackQuery):
		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(callback_query.from_user.id, f'Вы выбрали Наличные \
		, теперь отправьте {1} гривен на {1} или на {1} подождите после отправки 1 минуту и нажмите Проверить')




if __name__ == '__main__':
	db.start_db()
	executor.start_polling(dp, skip_updates=True)