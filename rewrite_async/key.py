from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

inline_kb_variant_addres = InlineKeyboardMarkup(row_width=2)
inline_btn_1 = InlineKeyboardButton('Координаты', callback_data='btn1')
inline_btn_2 = InlineKeyboardButton('Адрес', callback_data='btn2')
inline_kb_variant_addres.add(inline_btn_1, inline_btn_2)


bank_kb = InlineKeyboardMarkup(row_width=2)
mono = InlineKeyboardButton('Monobank', callback_data='monokey')
private = InlineKeyboardButton('PrivatBank', callback_data='privatekey')
bank_kb.add(mono, private)

payment_kb  = InlineKeyboardMarkup(row_width=2)
mono_pay = InlineKeyboardButton('Monobank', callback_data='mono_pay')
private_pay = InlineKeyboardButton('PrivatBank', callback_data='private_pay')
nal_pay = InlineKeyboardButton('Наличные', callback_data='nal_pay')
payment_kb.add(mono_pay, private_pay, nal_pay)


markup_key = ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
wether = KeyboardButton('погодка')
geo = KeyboardButton('геолока')
income = KeyboardButton('бюджет')
info = KeyboardButton('инфо')
price = KeyboardButton('цена')
date = KeyboardButton('дата')
be = KeyboardButton('я буду')
who_be = KeyboardButton('кто будет?')
dont_be = KeyboardButton('не буду')
pay = KeyboardButton('оплатить')
markup_key.add(wether,geo,income,info,price,date,be,who_be,dont_be,pay)