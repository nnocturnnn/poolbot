import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
geolocator = Nominatim(user_agent="tusabot")


url = 'https://api.privatbank.ua/p24api/infrastructure?json&tso&address=&city=%s' % ('Киев')    
req = requests.get(url).json()
location = geolocator.geocode("Киев Боголюбова 39", language='ru')
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
print(req['devices'][list_meters.index(min_meter)])
print(int(min_meter))


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