from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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