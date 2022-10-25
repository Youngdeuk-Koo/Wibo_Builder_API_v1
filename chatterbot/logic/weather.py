from chatterbot.logic import CustomAdapter
from chatterbot.functions import make_logic_response


from random import choice
import requests, json

class WeatherAdapter(CustomAdapter):
    URL_HEAD = 'https://api.openweathermap.org/data/2.5/weather?lat='
    OPENWEATHERMAP_APPID = "5c92a76854e6921d4c09d54bbb6cf30a"

    DICT_PATH = "chatterbot/logic/weather/"
 
    dict_response = json.load(open(DICT_PATH + "response.json"))
    dict_city2location = json.load(open(DICT_PATH + "city2location_2.json"))
    dict_weather2response = json.load(open(DICT_PATH + "weather2response.json"))


    def can_process(self, statement):
        return True


    def process(self, statement):
        print('-----weatehr process on-----')

        logic_name='weather_logic'

        user_info_url = 'https://mrmind.kr/mind/ai?id=' + str(self.chatbot.user_key)    # 유저키로 위도 경도
        data_user= requests.get(user_info_url)
        mrmind_info = json.loads(data_user.content)

        weather_info_url, flace_info = self.get_weather(statement, mrmind_info)
        data_weather = requests.get(weather_info_url)
        json_weather_info = json.loads(data_weather.content)

        address = flace_info[5]['formattedAddress'].split()

        weather_code = json_weather_info['weather'][0]['id']

        for x in self.dict_weather2response:
            
            if x['id'] == weather_code:

                if len(address) <= 2 :
                    response = x['comment'].format(address[0], address[1])
                    
                else:   
                    response = x['comment'].format(address[1], address[2])
                statement = make_logic_response(response, logic_name, statement)

        # statement.result['intent_id'] = 0
        statement.result['module'].insert(0, self.title)
        # statement.result['chatbot_id'] = self.chatbot_id
        
        return statement


    def get_weather(self, statement, mrmind_info):

        for text in statement.input['text'].split():
            if text in self.dict_city2location.keys():
                city = self.dict_city2location[text]
                weather_info_url = self.URL_HEAD + str(city['lat']) + '&lon=' + str(city['lon']) + '&appid=' + self.OPENWEATHERMAP_APPID 

                user_place_url = 'https://mrmind.kr/mind/geo?latitude=' + str(city['lat']) + '&longitude=' + str(city['lon']) # 위도 경도로 주소
                flace_user= requests.get(user_place_url)
                flace_info = json.loads(flace_user.content)

                return weather_info_url, flace_info

        weather_info_url = self.URL_HEAD + str(mrmind_info['profile']['latitude']) + '&lon=' + str(mrmind_info['profile']['longitude']) + '&appid=' + self.OPENWEATHERMAP_APPID
        user_place_url = 'https://mrmind.kr/mind/geo?latitude=' + str(mrmind_info['profile']['latitude']) + '&longitude=' + str(mrmind_info['profile']['longitude']) # 위도 경도로 주소
        flace_user= requests.get(user_place_url)
        flace_info = json.loads(flace_user.content)

        return weather_info_url, flace_info


