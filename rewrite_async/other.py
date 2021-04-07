import pyowm
import os

def pogodka():
	owm = pyowm.OWM(os.getenv('API_WEATHER'), language='ru')
	observation = owm.weather_at_place("Київ")
	w = observation.get_weather()
	temp = w.get_temperature('celsius')["temp"]

	pogodka = ("На тусовочке будет : " + w.get_detailed_status() 
			+ "\nТемпература около : " + str(temp) + " градусов")
	return pogodka

def get_mp4():
	pass