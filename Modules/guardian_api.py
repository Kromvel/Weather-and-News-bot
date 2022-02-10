import requests
import sys
sys.path.append("..")
from Modules import tokens as tk

API_KEY = tk.API_GUARDIAN_TOKEN

def parsing_guardian_news():
    params = {'api-key': API_KEY, 'page': 1}
    request_get = requests.get('https://content.guardianapis.com/search', params=params)

    data_response = request_get.json()
    news_list = data_response['response']['results']
    result = ""
    for i in news_list:
        result += '<b>' + i['sectionName'] + '</b>' + '\n'
        result += i['webTitle'] + '\n'
        result += '<a href="' + i['webUrl'] + '">Узнать подробности</a>' + '\n'
    return result
        
