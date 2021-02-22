import telebot
import time
import pyowm
import re
import datetime
import os
import requests
from xml.dom.minidom import parseString
from hashlib import md5,sha1
from requests import post
from geopy.geocoders import Nominatim
from telebot import apihelper
from scipy import spatial
from geopy.geocoders import Nominatim
import json

COMMANDS = ['Дом инфо','Инфо','Кто будет?','Геолока','Платежи','Погодка', 'Бюджет']
geolocator = Nominatim(user_agent="tusabot")
q = False
bot = telebot.TeleBot("1054227476:AAHMD3T4QOhQnJ1oBfLYaYI64Rx8O4dKWX8")
keyboard1 = telebot.types.ReplyKeyboardMarkup()
delkey = telebot.types.ReplyKeyboardRemove()
key1 = telebot.types.KeyboardButton('дом инфо')
key2 = telebot.types.KeyboardButton('инфо')
key3 = telebot.types.KeyboardButton('кто будет?')
key4 = telebot.types.KeyboardButton('геолока')
key5 = telebot.types.KeyboardButton('платежи')
key6 = telebot.types.KeyboardButton('бюджет')
key7 = telebot.types.KeyboardButton('погодка')
key8 = telebot.types.KeyboardButton('я буду')
key9 = telebot.types.KeyboardButton('кто скинул')
key10 = telebot.types.KeyboardButton('бляу у меня ток наличка')
keyboard1.row(key1, key2)
keyboard1.row(key3, key8)
keyboard1.row(key5, key6)
keyboard1.row(key7, key4)
keyboard1.row(key9, key10)


def terminal(message):
    message = message.text
    global q
    if message is not None:
        if message.startswith('&'):
            message += ' Киев' 
            url = 'https://api.privatbank.ua/p24api/infrastructure?json&tso&address=&city=%s' % ('Киев')    
            req = requests.get(url).json()
            location = geolocator.geocode(message, language='ru')
            if location is not None:
                lat = location.latitude
                lon = location.longitude
                A = [(lat, lon)]
                list_cord = []

                for i in range(len(req['devices'])):
                    lon_d = float(req['devices'][i]['latitude'])
                    lat_d = float(req['devices'][i]['longitude'])
                    B = (lat_d,lon_d)
                    list_cord.append(B)
                
                distance,index = spatial.KDTree(list_cord).query(A)
                with open('term.txt', 'w') as f:
                    f.write(str(list_cord[index[0]][0]))
                    f.write(' ')
                    f.write(str(list_cord[index[0]][1]))
                q = True

            

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


def privat_bank_payment(password,proxyDict, idi):
    sd = date_sd()
    ed = date_ed()
    url = "https://api.privatbank.ua/p24api/rest_fiz"

    head = """<?xml version="1.0" encoding="UTF-8"?>
    <request version="1.0">
    <merchant>
        <id>%s</id>
        <signature>""" % idi

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
    res = post(url, data=data_done, headers={'Content-Type': 'application/xml; charset=UTF-8'}, proxies=proxyDict)
    dom = parseString(res.text)
    # # Парсинг платежейs
    finalprint = ''
    payment = dom.getElementsByTagName('statement')
    leny = len(payment)
    i = 0
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
        if i == leny // 2:
            finalprint += '*'
    
    fp = ''
    for pay in payment:
        fp = pay.getAttribute('description') + ' - ' + pay.getAttribute('cardamount')
        q = open('whobe2.txt', 'r')
        alltext = q.read()
        if not finalprint in alltext:
            q.close()
            if fp.startswith('@'):
                f = open('whobe2.txt', 'a')
                f.write(fp)
                f.write('\n')
                f.close()
    
    return finalprint

def privat_bank (password,proxyDict,idi):

    url = "https://api.privatbank.ua/p24api/balance"

    head = """<?xml version="1.0" encoding="UTF-8"?>
    <request version="1.0">
    <merchant>
        <id>%s</id>
        <signature>""" % idi

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
    res = post(url, data=data_done, headers={'Content-Type': 'application/xml; charset=UTF-8'}, proxies=proxyDict)
    dom = parseString(res.text)
    # Парсинг баланса
    balancetag = dom.getElementsByTagName('balance')[0].toxml()
    balance = re.findall(r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?',balancetag)

    return balance[0]

def pogodka():
	owm = pyowm.OWM(os.getenv('API_WEATHER'), language='ru')
	observation = owm.weather_at_place("Київ")
	w = observation.get_weather()
	temp = w.get_temperature('celsius')["temp"]

	pogodka = ("На тусовочке будет : " + w.get_detailed_status() 
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

def get_home(message):
	f = open('home.txt', 'w')
	f.write(message.text)
	f.close()

def get_who(message):
	if not " " in message.text:
		q = open('whobe.txt', 'r')
		alltext = q.read()
		if not message.text in alltext:
			q.close()
			if message.text.startswith('@'):
				f = open('whobe.txt', 'a')
				f.write(message.text)
				f.write('\n')
				f.close()


def get_who2(message):
	q = open('whobe2.txt', 'r')
	alltext = q.read()
	if not message.text in alltext:
		q.close()
		if message.text.startswith('@'):
			f = open('whobe2.txt', 'a')
			f.write(message.text)
			f.write('\n')
			f.close()

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

@bot.message_handler(content_types = ['text'])
def main_option(message):
	proxyDict = { 
			"http"  : os.environ.get('FIXIE_URL', ''), 
			"https" : os.environ.get('FIXIE_URL', '')}
	if message.text.lower() == 'погодка':
		# bot.send_message(message.chat.id, pogodka(),reply_markup=delkey)
		bot.send_message(message.chat.id , "На тусовочке будет : ясно"
			+ "\nТемпература около : 32.5 градусов",reply_markup=delkey)
	elif message.text == 'дом инфо':
		f = open('home.txt', 'r')
		fd = f.read()
		try:
			bot.send_message(message.chat.id, fd,reply_markup=delkey)
		except:
			bot.send_message(message.chat.id, "поставь инфо пидор /setinfo",reply_markup=delkey)
		f.close()
	elif message.text.startswith('@') == True:
		get_who(message)
	elif message.text.lower() == 'бюджет':
		try:
			bot.send_message(message.chat.id, "Бюджет тусовочки 💴 💴 💴 " + privat_bank(os.getenv('API_PRIVAT'), proxyDict, "153753") + " грувнев",reply_markup=delkey)
		except:
			try:
				bot.send_message(message.chat.id, "Бюджет тусовочки 💴 💴 💴 " + privat_bank(os.getenv('API_PRIVAT2'),proxyDict, "155325") + " грувнев",reply_markup=delkey)
			except:
				bot.send_message(message.chat.id, 'Cервер выебываеться попробуйте позже 😔 😔 😔',reply_markup=delkey)
	elif message.text.lower() == 'я буду':
		bot.send_message(message.chat.id, "А теперь отправь свой ник !",reply_markup=delkey)
	elif message.text.lower() == 'инфо':
		f = open('info.txt', 'r')
		fd = f.read()
		try:
			bot.send_message(message.chat.id, fd,reply_markup=delkey)
		except:
			bot.send_message(message.chat.id, "поставь инфо пидор /setinfo",reply_markup=delkey)
		f.close()
	elif message.text.lower() == 'кто будет?':
		f = open('whobe.txt', 'r')
		whobefd = f.read()
		try:
			bot.send_message(message.chat.id, whobefd,reply_markup=delkey)
		except:
			bot.send_message(message.chat.id, "Никого",reply_markup=delkey)
		f.close()
	elif message.text.lower() == 'геолока':
		f = open('locate.txt', 'r')
		adresfd = f.read()
		try:
			location = geolocator.geocode(adresfd, language='ru')
			bot.send_location(message.chat.id, location.latitude, location.longitude)
		except:
			bot.send_message(message.chat.id, 'Cервер выебываеться попробуйте позже 😔 😔 😔',reply_markup=delkey)
		f.close()
	elif message.text.lower() == 'платежи':
		try:
			pri = privat_bank_payment(os.getenv('API_PRIVAT'),proxyDict, "153753")
			pri_list = pri.split('*')
			for i in pri_list:
				bot.send_message(message.chat.id, i ,reply_markup=delkey)
		except:
			pri = privat_bank_payment(os.getenv('API_PRIVAT2'),proxyDict, "155325")
			pri_list = pri.split('*')
			for i in pri_list:
				bot.send_message(message.chat.id, i ,reply_markup=delkey)
	elif message.text.lower() == 'ip':
		rer = requests.get('https://ramziv.com/ip', proxies=proxyDict).text
		bot.send_message(message.chat.id, rer,reply_markup=delkey)
	elif message.text.lower() == 'rm -rf':
		f = open('whobe.txt','w')
		f.close()
	elif message.text.lower() == 'бляу у меня ток наличка':
		bot.send_message(message.chat.id, "А теперь отправь свой адрес формата &Хрещатик 12",reply_markup=delkey)
		global q
		while q == False:
			bot.register_next_step_handler(message, terminal)
			time.sleep(4)
		with open('term.txt', 'r') as f:
			lonlat = f.read().split()
			try:
				bot.send_message(message.chat.id, "А теперь сучара получи ближайший терминал без коммисии !\nПиздуй пополняй",reply_markup=delkey)
				bot.send_location(message.chat.id, lonlat[0], lonlat[1])
				q = False
			except:
				bot.send_message(message.chat.id, "Введи нормальный адрес")
		f = open('term.txt','w')
		f.close()
	elif message.text.lower() == 'скинул':
		bot.register_next_step_handler(message, get_who2)
	elif message.text.lower() == 'check':
		try:
			bot.send_message(message.chat.id, privat_bank_payment(os.getenv('API_PRIVAT'),proxyDict, "153753"),reply_markup=delkey)
		except:
			bot.send_message(message.chat.id, privat_bank_payment(os.getenv('API_PRIVAT2'),proxyDict, "155325"),reply_markup=delkey)
	elif message.text.lower() == 'кто скинул':
		f = open('whobe2.txt', 'r')
		whobefd = f.read()
		try:
			bot.send_message(message.chat.id, whobefd,reply_markup=delkey)
		except:
			bot.send_message(message.chat.id, "Никто",reply_markup=delkey)
		f.close()

bot.polling(none_stop=True)
