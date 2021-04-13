import logging
import banking
import other
import db
import key as kb
import os
import requests
from geopy.geocoders import Nominatim
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import BoundFilter


API_TOKEN = os.getenv('API_TELEGRAM')
logging.basicConfig(level=logging.INFO)
geolocator = Nominatim(user_agent="tusabot")
delkey = kb.ReplyKeyboardRemove()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot,storage=MemoryStorage())

#                  _               _                                               
#      /\         | |             (_)               /\                             
#     /  \      __| |  _ __ ___    _   _ __        /  \     ___   ___    ___   ___ 
#    / /\ \    / _` | | '_ ` _ \  | | | '_ \      / /\ \   / __| / __|  / _ \ / __|
#   / ____ \  | (_| | | | | | | | | | | | | |    / ____ \  \__ \ \__ \ |  __/ \__ \
#  /_/    \_\  \__,_| |_| |_| |_| |_| |_| |_|   /_/    \_\ |___/ |___/  \___| |___/

class MyFilter(BoundFilter):
	key = 'is_admin'

	def __init__(self, is_admin):
		self.is_admin = is_admin

	async def check(self, message: types.Message):
		member = await bot.get_chat_member(message.chat.id, message.from_user.id)
		return member.is_chat_admin()

dp.filters_factory.bind(MyFilter)

#    _____   _             _                
#   / ____| | |           | |               
#  | (___   | |_    __ _  | |_    ___   ___ 
#   \___ \  | __|  / _` | | __|  / _ \ / __|
#   ____) | | |_  | (_| | | |_  |  __/ \__ \
#  |_____/   \__|  \__,_|  \__|  \___| |___/


class Test(StatesGroup):
	info = State()
	locale = State()
	date = State()
	price = State()
	cardprivate = State()
	cardmono = State()
	term = State()

@dp.message_handler(state=Test.term)
async def term_state(message: types.Message, state: FSMContext):
	answer = message.text
	text, lon_lat = banking.get_near_terminal(answer)
	await message.answer(text)
	await message.answer_location(lon_lat[1],lon_lat[0])
	await state.finish()


@dp.message_handler(state=Test.info)
async def info_state(message: types.Message, state: FSMContext):
	answer = message.text
	db.insert_db(message.chat.id,info=answer)
	await bot.unpin_all_chat_messages(message.chat.id)
	await bot.pin_chat_message(message.chat.id, message.message_id)
	await state.finish()
	await message.answer("Информация успешно установлена")

@dp.message_handler(state=Test.locale)
async def locale_state(message: types.Message, state: FSMContext):
	answer = message.text
	db.insert_db(message.chat.id,locale=answer)
	await state.finish()
	await message.answer("Геолокация успешно установлена")

@dp.message_handler(state=Test.date)
async def date_state(message: types.Message, state: FSMContext):
	answer = message.text
	db.insert_db(message.chat.id,date=answer.lower())
	await state.finish()
	await message.answer("Дата успешно установлена")

@dp.message_handler(state=Test.price)
async def price_state(message: types.Message, state: FSMContext):
	answer = message.text
	db.insert_db(message.chat.id,price=answer.lower())
	await state.finish()
	await message.answer("Цена успешно установлена")

@dp.message_handler(state=Test.cardprivate)
async def cardprivate_state(message: types.Message, state: FSMContext):
	answer = message.text
	db.insert_db(message.chat.id,private=answer)
	await state.finish()
	await message.answer("Информация успешно установлена")

@dp.message_handler(state=Test.cardmono)
async def ccardmono_state(message: types.Message, state: FSMContext):
	answer = message.text
	db.insert_db(message.chat.id,mono=answer)
	await state.finish()
	await message.answer("Информация успешно установлена")



#   _    _                       _   _                     
#  | |  | |                     | | | |                    
#  | |__| |   __ _   _ __     __| | | |   ___   _ __   ___ 
#  |  __  |  / _` | | '_ \   / _` | | |  / _ \ | '__| / __|
#  | |  | | | (_| | | | | | | (_| | | | |  __/ | |    \__ \
#  |_|  |_|  \__,_| |_| |_|  \__,_| |_|  \___| |_|    |___/


@dp.message_handler(is_admin=True,commands=['start', 'help', 'setinfo',
					'setlocale', 'setdate', 'setprice','setcardinfo','delete'])
async def send_command(message: types.Message):
	if message.text.lower().startswith('/start'):
		db.insert_db(message.chat.id)
		await message.answer( f'{message.from_user.first_name} , добро \
пожаловать к PartyBot!\nЕсть вопросы? Обратись к помощи /help\n')
	elif message.text.lower() == "/help":
		await message.answer("Этот бот поможет организовать тусовочку\n\
/setinfo - установить информацию тусовочки\n/setlocale - установить место\n\
/setdate - установить дату\n/setprice - установить цену\n/setcardinfo \
		- установить автопроверку платежей (Monobank, PrivatBank)")
	elif message.text.lower() == "/setinfo":
		await message.answer("А теперь отправь информацию о тусовочке!")
		await Test.info.set()
	elif message.text.lower() == "/setlocale":
		kb.inline_btn_1.callback_data = "btn1 " + str(message.message_id) + " " + str(message.from_user.id)
		kb.inline_btn_2.callback_data = "btn2 " + str(message.message_id) + " "  + str(message.from_user.id)
		await message.answer("А теперь выбери формат адреса",reply_markup=kb.inline_kb_variant_addres)
	elif message.text.lower() == "/setdate":
		await message.answer("А теперь отправь дату тусовочки!\nНапример 17.03")
		await Test.date.set()
	elif message.text.lower() == "/setprice":
		await message.answer("А теперь отправь стоимость проходки на тусовочку!")
		await Test.price.set()
	elif message.text.lower() == "/setcardinfo":
		kb.mono.callback_data = "monokey " + str(message.message_id) + " " + str(message.from_user.id)
		kb.private.callback_data = "privatekey " + str(message.message_id) + " "  + str(message.from_user.id)
		await message.answer("А теперь выбери свой банк!",reply_markup=kb.bank_kb)
	elif message.text.lower().startswith("/delete"):
		str_to_db = db.get_from_db(str(message.chat.id),"list_user")
		user = message.text.split()[1]
		if str_to_db.find(user) == -1:
			await message.answer(user + " - нет в списке")
		else:
			str_to_db = str_to_db.replace(user + "\n","")
			db.insert_db(message.chat.id,list_user=str_to_db)
			await message.answer(user + " - удалил из списка")


@dp.message_handler(content_types = ['text'])
async def send_text(message: types.Message):
	m_id = message.chat.id
	proxyDict = {
		"http"  : os.environ.get('FIXIE_URL', ''), 
		"https" : os.environ.get('FIXIE_URL', '')}
	if message.text.lower() == 'погодка':
		try:
			await message.answer(other.pogodka(m_id),reply_markup=delkey)
		except:
			await message.answer("Погодка будет доступна за 5 дней до туссовки.",reply_markup=delkey)
	elif message.text.startswith('/key'):
		await message.answer("Вот мои комманды: ",reply_markup=kb.markup_key)
	elif message.text.lower() == 'дата':
		await message.answer(db.get_from_db(str(m_id),"date"),reply_markup=delkey)
	elif message.text.lower() == 'цена':
		await message.answer(db.get_from_db(str(m_id),"price") + " ₴",reply_markup=delkey)
	elif message.text.lower() == 'инфо':
		await message.answer(db.get_from_db(str(m_id),"info"),reply_markup=delkey)
	elif message.text.lower() == 'кто будет?':
		await message.answer(db.get_from_db(str(m_id),"list_user"),reply_markup=delkey)
	elif message.text.lower() == 'я буду':
		str_to_db = db.get_from_db(str(m_id),"list_user")
		user = message.from_user.username
		if user is None:
			user = message.from_user.full_name
		if str_to_db.find(user) == -1:
			if str_to_db == "none":
				db.insert_db(m_id,list_user= "@" + user + "\n")
			else:
				db.insert_db(m_id,list_user=str_to_db + "@" + user + "\n")
			await message.answer("@" + user + " - добавил тебя в список",reply_markup=delkey)
		else:
			await message.answer("@" + user + " - извини но ты уже в списке",reply_markup=delkey)
	elif message.text.lower() == 'не буду':
		str_to_db = db.get_from_db(str(m_id),"list_user")
		user = message.from_user.username
		if user is None:
			user = message.from_user.full_name
		if str_to_db.find(user) == -1:
			await message.answer("@" + user + " - тебя нет в списке",reply_markup=delkey)
		else:
			str_to_db = str_to_db.replace("@" + user + "\n","")
			db.insert_db(m_id,list_user=str_to_db)
			await message.answer("@" + user + " - удалил тебя из списка",reply_markup=delkey)
	elif message.text.lower() == 'геолока':
		locale = db.get_from_db(str(m_id),"locale").strip()
		if locale[0].isdigit():
			await message.answer_location(locale.split()[0],locale.split()[1])
		else:
			location = geolocator.geocode(locale, language='ru')
			await message.answer(location,reply_markup=delkey)
			await message.answer_location(location.latitude, location.longitude)
	elif message.text.lower() == 'бюджет':
		try:
			# p_price = privat_bank(os.getenv('API_PRIVAT2'),proxyDict, "155325","5168745302334229")
			m_price = int(banking.mono_bank(m_id))
			await message.answer("Бюджет тусовочки 💴 💴 💴 : " + str(m_price) + " ₴",reply_markup=delkey)
		except:
			await message.answer('Cервер выебываеться попробуйте позже 😔 😔 😔',reply_markup=delkey)
	elif message.text.lower() == 'оплатить':
		kb.mono_pay.callback_data = "mono_pay " + str(message.message_id) + " " + str(message.from_user.id)
		kb.private_pay.callback_data = "private_pay " + str(message.message_id) + " " + str(message.from_user.id)
		kb.nal_pay.callback_data = "nal_pay " + str(message.message_id) + " " + str(message.from_user.id)
		await message.answer("Выберите способ оплаты :",reply_markup=kb.payment_kb)
	# elif message.text.lower() == 'ip':
	# 	rer = requests.get('https://ramziv.com/ip', proxies=proxyDict).text
	# 	await message.answer(rer)




#   _____           _   _                    _  __                     
#  |_   _|         | | (_)                  | |/ /                     
#    | |    _ __   | |  _   _ __     ___    | ' /    ___   _   _   ___ 
#    | |   | '_ \  | | | | | '_ \   / _ \   |  <    / _ \ | | | | / __|
#   _| |_  | | | | | | | | | | | | |  __/   | . \  |  __/ | |_| | \__ \
#  |_____| |_| |_| |_| |_| |_| |_|  \___|   |_|\_\  \___|  \__, | |___/
#                                                           __/ |      
#                                                          |___/       

@dp.callback_query_handler(lambda c: c.data.startswith('btn1'))
async def process_callback_button1(callback_query: types.CallbackQuery):
	cb_m_id = callback_query.message.chat.id
	if callback_query.data.endswith(str(callback_query.from_user.id)):
		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(cb_m_id, 'Вы выбрали координаты, теперь \
отправьте lontitude latitude\nНапример 50.32434 47.32443')
		await Test.locale.set()
		data = int(callback_query.data.split()[1]) + 1
		await bot.edit_message_reply_markup(cb_m_id, data)
			

@dp.callback_query_handler(lambda c: c.data.startswith('btn2'))
async def process_callback_button2(callback_query: types.CallbackQuery):
	cb_m_id = callback_query.message.chat.id
	if callback_query.data.endswith(str(callback_query.from_user.id)):
		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(cb_m_id, 'Вы выбрали адрес, теперь \
отправьте адрес\nНапример Киев Хрещатик 4')
		await Test.locale.set()
		data = int(callback_query.data.split()[1]) + 1
		await bot.edit_message_reply_markup(cb_m_id, data)

@dp.callback_query_handler(lambda c: c.data.startswith('monokey'))
async def process_callback_mono(callback_query: types.CallbackQuery):
	cb_m_id = callback_query.message.chat.id
	if callback_query.data.endswith(str(callback_query.from_user.id)):
		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(cb_m_id, 'Вы выбрали Монобанк \
, теперь отправьте токен монобанка и номер карты\nНапример Adf42sdf2342442sdf2314432 4441114446179218\n\
Чтобы получить токен монобанка перейдите по ссылке https://api.monobank.ua/')
		await Test.cardmono.set()
		data = int(callback_query.data.split()[1]) + 1
		await bot.edit_message_reply_markup(cb_m_id, data)

@dp.callback_query_handler(lambda c: c.data.startswith('privatekey'))
async def process_callback_private(callback_query: types.CallbackQuery):
	cb_m_id = callback_query.message.chat.id
	if callback_query.data.endswith(str(callback_query.from_user.id)):
		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(cb_m_id, 'Вы выбрали Приватбанк\
, теперь отправьте токен и номер карты\nНапример Adf42sdf2342442sdf2314432 4441114446179218 \n\
Чтобы получить токен приватбанка перейдите по ссылке https://api.privatbank.ua/#p24/registration')
		await Test.cardprivate.set()
		data = int(callback_query.data.split()[1]) + 1
		await bot.edit_message_reply_markup(cb_m_id, data)

@dp.callback_query_handler(lambda c: c.data.startswith('private_pay'))
async def process_callback_private_pay(callback_query: types.CallbackQuery):
	cb_m_id = callback_query.message.chat.id
	if callback_query.data.endswith(str(callback_query.from_user.id)):
		await bot.answer_callback_query(callback_query.id)
		info = db.get_from_db(cb_m_id, "private")
		price = db.get_from_db(cb_m_id, "price")
		data = callback_query.data.split()
		kb.check_b.callback_data = "check_pay " + str(callback_query.message.message_id) + " " + data[2]
		if info == "none":
			await bot.send_message(cb_m_id ,"К сожалению Приватбанк не был подключен")
		else:
			card_num = info.split()[1]
			await bot.send_message(cb_m_id, f'Вы выбрали Приватбанк, теперь \
отправьте больше {price} гривен на {card_num} и укажите свой ник в комментарии к \
платежу . После отправки нажмите Проверить')
		await bot.edit_message_reply_markup(cb_m_id, int(data[1]) + 1)

@dp.callback_query_handler(lambda c: c.data.startswith('mono_pay'))
async def process_callback_mono_pay(callback_query: types.CallbackQuery):
	cb_m_id = callback_query.message.chat.id
	if callback_query.data.endswith(str(callback_query.from_user.id)):
		await bot.answer_callback_query(callback_query.id)
		info = db.get_from_db(cb_m_id,"mono")
		price = db.get_from_db(cb_m_id,"price")
		data = callback_query.data.split()
		kb.check_b.callback_data = "check_pay " + str(callback_query.message.message_id) + " " + data[2]
		if info == "none":
			await bot.send_message(cb_m_id,"К сожалению Монобанк не был подключен",reply_markup=kb.check_kb)
		else:
			card_num = info.split()[1]
			await bot.send_message(cb_m_id, f'Вы выбрали Монобанк, теперь \
отправьте больше {price} гривен на {card_num} и укажите свой ник в комментарии к \
платежу . После отправки нажмите Проверить',reply_markup=kb.check_kb)
		await bot.edit_message_reply_markup(cb_m_id, int(data[1]) + 1)

@dp.callback_query_handler(lambda c: c.data.startswith('nal_pay'))
async def process_callback_nal_pay(callback_query: types.CallbackQuery):
	cb_m_id = callback_query.message.chat.id
	if callback_query.data.endswith(str(callback_query.from_user.id)):
		await bot.send_message(cb_m_id, "Теперь отправь свой адрес, например Антонова 43")
		await Test.term.set()
		await bot.answer_callback_query(callback_query.id)
		info_mono = db.get_from_db(cb_m_id,"mono")
		info_private = "none"
		if info_mono == "none":
			card_num = info_mono
		else:
			card_num = info_mono.split()[1]
		price = db.get_from_db(cb_m_id,"price")
		data = callback_query.data.split()
		kb.check_b.callback_data = "check_pay " + str(callback_query.message.message_id) + " " + data[2]
		await bot.send_message(cb_m_id, f'Вы выбрали Наличные, теперь отправьте \
больше {price} гривен на {card_num} или на {info_private} и укажите свой ник в \
комментарии к платежу подождите после отправки 1 минуту и нажмите Проверить',reply_markup=kb.check_kb)
		await bot.edit_message_reply_markup(cb_m_id, int(data[1]) + 1)


@dp.callback_query_handler(lambda c: c.data.startswith('check_pay'))
async def process_callback_check_pay(callback_query: types.CallbackQuery):
	cb_m_id = callback_query.message.chat.id
	if callback_query.data.endswith(str(callback_query.from_user.id)):
		last_tr = banking.mono_check(cb_m_id)
		if int(db.get_from_db(cb_m_id, "price")) <= last_tr['amount'] / 100:
			str_to_db = db.get_from_db(str(cb_m_id),"list_user")
			try:
				user = last_tr['comment'] + "✅"
				not_done = last_tr['comment']
				if str_to_db == "none":
					db.insert_db(cb_m_id,list_user= user + "\n")
				elif str_to_db.find(not_done) > -1:
					db.insert_db(cb_m_id,list_user=str_to_db.replace(not_done,user))
					await bot.send_message(cb_m_id,"Oплата прошла успешно")
				elif str_to_db.find(user) == -1:
					db.insert_db(cb_m_id,list_user=str_to_db + user + "\n")
					await bot.send_message(cb_m_id,"Oплата прошла успешно")
				else:
					await bot.send_message(cb_m_id,"Oплата не прошла, обратитесь к админу")
			except:
				await bot.send_message(cb_m_id,"Oплата не прошла, обратитесь к админу")
		else:
			await bot.send_message(cb_m_id,"Oплата не прошла, обратитесь к админу")
		data = callback_query.data.split()
		await bot.edit_message_reply_markup(cb_m_id, int(data[1]) + 1)





if __name__ == '__main__':
	db.start_db()
	executor.start_polling(dp, skip_updates=True)