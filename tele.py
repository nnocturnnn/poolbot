import telebot
import time
import pyowm
import configparser
import re
import datetime
import os
from xml.dom.minidom import parseString
from hashlib import md5,sha1
from requests import post
from geopy.geocoders import Nominatim

COMMANDS = ['Дом инфо','Инфо','Кто будет?','Геолока','Платежи','Погодка', 'Бюджет']

# config = configparser.ConfigParser()
# config.read("config.ini")
geolocator = Nominatim(user_agent="tusabot")
bot = telebot.TeleBot(os.getenv("API_TELEGRAM"))
keyboard1 = telebot.types.ReplyKeyboardMarkup()
key1 = telebot.types.KeyboardButton('дом инфо')
key2 = telebot.types.KeyboardButton('инфо')
key3 = telebot.types.KeyboardButton('кто будет ?')
key4 = telebot.types.KeyboardButton('геолока')
key5 = telebot.types.KeyboardButton('платежи')
key6 = telebot.types.KeyboardButton('бюджет')
key7 = telebot.types.KeyboardButton('погодка')
key8 = telebot.types.KeyboardButton('/я буду')
keyboard1.row(key1, key2)
keyboard1.row(key3, key8)
keyboard1.row(key5, key6)
keyboard1.row(key7, key4)

def date_sd():
    now = datetime.datetime.now()
    month = now.month - 1
    year = now.year
    if month == 0:
        month = 12
        year -= 1
    sd = str(now.day) + '.'
    if month < 10:
        sd += '0' 
    sd += str(month) + '.' + str(year)
    return sd

def date_ed():
    now = str(datetime.datetime.now()).split()[0]
    edlist = now.split('-')
    edlist.reverse()
    ed = '.'.join(edlist)
    return ed


def privat_bank_payment(password):
    sd = date_sd()
    ed = date_ed()
    url = "https://api.privatbank.ua/p24api/rest_fiz"

    head = """<?xml version="1.0" encoding="UTF-8"?>
    <request version="1.0">
    <merchant>
        <id>153753</id>
        <signature>"""

    data = """<oper>cmt</oper>
        <wait>0</wait>
        <test>0</test>
        <payment id="">
            <prop name="sd" value="%s" />
            <prop name="ed" value="%s" />
            <prop name="card" value="5168745302334229" />
        </payment>""" % (sd, ed)

    end_head = """</signature>
    </merchant>
    <data>
        """

    footer = """
    </data>
    </request>"""

    # === Шифрование Ключа ====================================
    signature_md5 = md5((data+password).encode('utf-8')).hexdigest()
    signature_done = sha1(signature_md5.encode('utf-8')).hexdigest()

    data_done = head + signature_done + end_head + data + footer

    # === Запрос
    res = post(url, data=data_done, headers={'Content-Type': 'application/xml; charset=UTF-8'})
    dom = parseString(res.text)
    # # Парсинг платежейs
    finalprint = ''
    payment = dom.getElementsByTagName('statement')
    for pay in payment:
        finalprint += ' 💳 💳 💳 '
        finalprint += pay.getAttribute('trandate')
        finalprint += ' : '
        finalprint += pay.getAttribute('cardamount')
        finalprint += ' : '
        try:
            finalprint += pay.getAttribute('description')
        except:
            finalprint += ' '
        finalprint += '\n'
    
    return finalprint

def privat_bank (password):

    url = "https://api.privatbank.ua/p24api/balance"

    head = """<?xml version="1.0" encoding="UTF-8"?>
    <request version="1.0">
    <merchant>
        <id>153753</id>
        <signature>"""

    data = """<oper>cmt</oper>
        <wait>0</wait>
        <test>0</test>
        <payment id="">
        <prop name="cardnum" value="5168745302334229" />
        <prop name="country" value="UA" />
        </payment>"""

    end_head = """</signature>
    </merchant>
    <data>
        """

    footer = """
    </data>
    </request>"""

    # === Шифрование Ключа ====================================
    signature_md5 = md5((data+password).encode('utf-8')).hexdigest()
    signature_done = sha1(signature_md5.encode('utf-8')).hexdigest()

    data_done = head + signature_done + end_head + data + footer

    # === Запрос
    res = post(url, data=data_done, headers={'Content-Type': 'application/xml; charset=UTF-8'})
    dom = parseString(res.text)
    # Парсинг баланса
    balancetag = dom.getElementsByTagName('balance')[0].toxml()
    balance = re.findall(r'\d.\d{2}',balancetag)

    return balance[0]

def pogodka():
	owm = pyowm.OWM(os.getenv("API_WEATHER"), language='ru')
	observation = owm.weather_at_place("Київ")
	w = observation.get_weather()
	temp = w.get_temperature('celsius')["temp"]

	pogodka = ("В Кийове сейчас : " + w.get_detailed_status() 
			+ "\nТемпература около : " + str(temp) + " градусов")
	return pogodka

def setinfo(message):
    a = message.split(' ', maxsplit = 1)[1]
    return a

def get_info(message):
	f = open('info.txt', 'w')
	f.write(message.text)
	f.close()

def get_locate(message):
	f = open('locate.txt', 'w')
	f.write(message.text)
	f.close()

def get_who(message):
	f = open('whobe.txt', 'a')
	f.write(message.text)
	f.close


@bot.message_handler(commands = ['start', 'help', 'fullhelp', 'setinfo', '/я буду', 'setlocate'])
def handle_start_help(message):
	if message.text == "/start":
		bot.send_message(message.chat.id, "Привет, чем я могу тебе помочь?", reply_markup=keyboard1)
	elif message.text == "/help":
		bot.send_message(message.chat.id, "Вот список моих команд: " 
				+ ', '.join(COMMANDS) + ". Просто напиши любую из них")
	elif message.text == "/fullhelp":
		bot.send_message(message.chat_id, "")
	elif message.text == '/setinfo':
		bot.send_message(message.chat.id, "А сейчас отправь инфу !")
		bot.register_next_step_handler(message, get_info)
	elif message.text == '/я буду':
		bot.send_message(message.chat.id, "А теперь отправь свой ник !")
		bot.register_next_step_handler(message, get_who)
	elif message.text == '/setlocate':
		bot.send_message(message.chat.id, "А сейчас отправь адрес !")
		bot.register_next_step_handler(message, get_locate)

@bot.message_handler(content_types = ['text'])
def main_option(message):
	if message.text.lower() == 'погодка':
		bot.send_message(message.chat.id, pogodka())
	elif message.text.lower() == 'бюджет':
		bot.send_message(message.chat.id, "Бюджет тусовочки 💴 💴 💴 " 
		+ privat_bank(os.getenv("API_PRIVAT")) + " грувнев")
	elif message.text.lower() == 'инфо':
		f = open('info.txt', 'r')
		fd = f.read()
		bot.send_message(message.chat.id, fd)
		f.close()
	elif message.text.lower() == 'кто будет?':
		f = open('info.txt', 'r')
		whobe = f.read()
		bot.send_message(message.chat.id, whobe)
		f.close()
	elif message.text.lower() == 'геолока':
		f = open('locate.txt', 'r')
		adres = f.read()
		location = geolocator.geocode(adres, language='ru')
		bot.send_location(message.chat.id, location.latitude, location.longitude)
		f.close()
	elif message.text.lower() == 'платежи':
		bot.send_message(message.chat.id, privat_bank_payment(os.getenv("API_PRIVAT")))
	# elif message.text.lower() == 'дом инфа':
	# 	bot.send_message(message.chat.id, house_info())


bot.polling(none_stop=True)
