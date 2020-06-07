import requests
from scipy import spatial
from geopy.geocoders import Nominatim
import pprint
import json

geolocator = Nominatim(user_agent="tusabot")

def terminal(message):
    message = message.text
    url = 'https://api.privatbank.ua/p24api/infrastructure?json&tso&address=&city=%s' % ('Киев')    
    req = requests.get(url).json()
    location = geolocator.geocode('Доброхотова 14', language='ru')
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
    f = open('term.txt', 'w')
    f.write(str(list_cord[index[0]][0]))
    f.write(' ')
    f.write(str(list_cord[index[0]][1]))
    f.close()

terminal('fdf')
f = open('term.txt', 'r')
lonlat = f.read().split()
print(lonlat[0])