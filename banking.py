import requests
import datetime
import re
from datetime import date
from hashlib import md5,sha1
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from xml.dom.minidom import parseString
import monobank
import db

geolocator = Nominatim(user_agent="tusabot")

def get_near_terminal(message):
    url = 'https://api.privatbank.ua/p24api/infrastructure?json&tso&address=&city=%s' % ('Киев')    
    req = requests.get(url).json()
    location = geolocator.geocode(message, language='ru')
    addres_lat_lon = (location.latitude, location.longitude)
    list_cord = []
    list_meters = []
    for i in range(len(req['devices'])):
        lon_d = float(req['devices'][i]['latitude'])
        lat_d = float(req['devices'][i]['longitude'])
        all_lat_lon = (lat_d,lon_d)
        list_cord.append(all_lat_lon)

    for i in list_cord:
        list_meters.append(geodesic(addres_lat_lon, i).meters)
    min_meter = min(list_meters)
    need_device = req['devices'][list_meters.index(min_meter)]
    ret_str = f"К близжайшему терминалу {int(min_meter)} м. он в {need_device['placeRu']}"
    addres_lat_lon = (need_device['latitude'],need_device['longitude'])
    return ret_str, addres_lat_lon


def date_sd():
    time_now = datetime.datetime.now() - datetime.timedelta(days=30)
    str_time = time_now.strftime("%m.%d.%Y")
    return str_time

def date_ed():
    time_now = datetime.datetime.now()
    str_time = time_now.strftime("%m.%d.%Y")
    return str_time


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
    res = requests.post(url, data=data_done, headers={'Content-Type': 'application/xml; charset=UTF-8'}, proxies=proxyDict)
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

def privat_bank(password,proxyDict,idi,card):

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
        <prop name="cardnum" value="%s" />
        <prop name="country" value="UA" />
        </payment>""" % card

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
    res = requests.post(url, data=data_done, headers={'Content-Type': 'application/xml; charset=UTF-8'}, proxies=proxyDict)
    dom = parseString(res.text)
    # Парсинг баланса
    balancetag = dom.getElementsByTagName('balance')[0].toxml()
    balance = re.findall(r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?',balancetag)

    return balance[0]


def mono_bank(char_id):
    token = db.get_from_db(char_id,"mono").split()[0]
    mono = monobank.Client(token)
    user_info = mono.get_client_info()
    for i in user_info['accounts']:
        if i['type'] == 'white':
            return i['balance'] / 100


def mono_check(char_id):
    token = db.get_from_db(char_id,"mono").split()[0]
    mono = monobank.Client(token)
    user_info = mono.get_client_info()
    id_w = ""
    for i in user_info['accounts']:
        if i['type'] == 'white':
            id_w = i['id']
    time_now = datetime.datetime.now()
    time_p = datetime.datetime.now() - datetime.timedelta(days=1)
    stat = mono.get_statements(id_w, time_p, time_now)
    return stat[0]
