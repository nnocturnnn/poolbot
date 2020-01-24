from xml.dom.minidom import parseString
from hashlib import md5,sha1
from requests import post
import re
import datetime

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

