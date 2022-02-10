# Узнать погоду в городе
import pyowm
import sys
sys.path.append("..")
from Modules import tokens as tk
from pyowm.utils.config import get_default_config

OWM_TOKEN = tk.OWM_TOKEN
CONFIG_DICT = get_default_config()
CONFIG_DICT['language'] = 'ru'
# Токен от api Openweather
OWM = pyowm.OWM(OWM_TOKEN,CONFIG_DICT)
MGR = OWM.weather_manager()


# Получение данных о погоде через api
def get_weather(message):
    try:
        #global greeting_2
        #greeting_2 = '\nЧто бы вы еще хотели узнать?'
        observation = MGR.weather_at_place(message)
        weather = observation.weather
        weather.status           # short version of status (eg. 'Rain')
        weather.detailed_status 
        temp_dict_celsius = weather.temperature('celsius')
        answer = "Сейчас в городе " + message + " температура " + str(round(temp_dict_celsius['temp'], 1)) +' °C' +', ощущается как ' + str(round(temp_dict_celsius['feels_like'], 1)) + ' °C' + ", " + weather.detailed_status
        return answer
    except Exception as e:
        #b.bot.send_message(message.chat.id, 'Город не найден :(\nПопробуйте еще раз или вернитесь в меню', reply_markup=b.mark_up_4)
        return 'Город не найден :(\nПопробуйте еще раз или можете узнать последние новости'
'''
message = "Moscow"
print(OWM)
print(MGR)  
obs_obj = MGR.weather_at_place('Москва')
print(obs_obj.weather.temperature('celsius'))
#get_weather(message)
'''