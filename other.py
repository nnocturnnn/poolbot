from pyowm import OWM
from datetime import datetime
from pyowm.utils.config import get_default_config
import db
import os

config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM(os.getenv('API_WEATHER'), config_dict)
mgr = owm.weather_manager()

def pogodka(chat_id):
    date = db.get_from_db(chat_id, "date").split('.')
    locale = db.get_from_db(str(chat_id),"locale").strip()
    observation = mgr.forecast_at_coords(float(locale.split()[0]),float(locale.split()[1]),'3h').forecast
    need_d = datetime(2021,int(date[1]),int(date[0]),12).strftime("%m/%d/%Y %H:%M")
    for i in observation:
        if need_d == i.reference_time('date').strftime("%m/%d/%Y %H:%M"):
            temp = i.temperature("celsius")
            status = i.detailed_status
            return f"На тусовочке будет {status} - {temp['temp']} градусов."
        