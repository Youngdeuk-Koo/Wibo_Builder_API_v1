from chatterbot.logic import CustomAdapter
from chatterbot.functions import make_response
from chatterbot import response_selection

from random import choice
import requests, json

class WeatherAdapter(CustomAdapter):

    OPENWEATHERMAP_APPID = "5c92a76854e6921d4c09d54bbb6cf30a"

    DICT_PATH = "chatterbot/logic/weather/"
    dict_intents_cmd = json.load(open(DICT_PATH + "intents_cmd.json"))
    dict_intents = json.load(open(DICT_PATH + "intents.json"))
    dict_intents_keyword = json.load(open(DICT_PATH + "intents_keyword.json"))
    dict_response = json.load(open(DICT_PATH + "response.json"))
    dict_code2response = json.load(open(DICT_PATH + "code2response.json"))
    dict_province2city = json.load(open(DICT_PATH + "province2city.json"))
    dict_city2location = json.load(open(DICT_PATH + "city2location.json"))

    def can_process(self, statement):
        return True

    def process(self, statement, intent=None):
        print('-----weatehr process on-----')

        if intent is None:
            intent, confidence = self.recognize_intent(statement)
        else:
            confidence = 1.0

        if intent is not None:
            input_text = statement.input['text']
            print('@@@@@@@@@@@@@@@@@@@@@@@---weather input_text', input_text)
            if intent == "request_weather":
                remote_addr = statement.request.get('remote_addr', None)
                statement.context['variables'].update(
                    {'weather_info': self.get_weather_info(input_text, remote_addr, statement)}
                )

            intentnode_id = self.chatbot.storage.get_custom_intent_node_id_for_text(self.id, intent)
            print('@@@@@@@@@@@@@@@@@@@@@@@---weather input_text', input_text)
            if intentnode_id is not None:
                response_groups = self.chatbot.storage.get_custom_response_groups(intentnode_id)
                response_group = choice(response_groups)
                for response in response_group['data']:
                    statement = make_response(response, statement)
            else:
                _text = choice(self.dict_response[intent])
                for _key, _value in statement.context['variables'].items():
                    _text = _text.replace('{' + _key + '}', _value)
                statement.output.append({"text": _text})

            statement.result['module'].insert(0, self.title)
            statement.result['intent'].insert(0, intent)
            statement.result['confidence'] = confidence
            statement.result['confidence_property'] = 'weather_locgic'

        return statement


    def recognize_intent(self, statement):
        input_text = statement.input['text']

        # cmd
        for _intent, _samples in self.dict_intents_cmd.items():
            for sample in _samples:
                if input_text == sample:
                    return _intent, 1.0

        # check keyword
        intent = None
        keyword = None
        for _intent, _samples in self.dict_intents_keyword.items():
            for sample in _samples:
                _keyword = sample.replace(' ', '')
                if _keyword in input_text:
                    intent = _intent
                    keyword = _keyword
                    break
            if keyword is not None:
                break

        # if input_text == keyword:
        #     intent = intent.replace('request', 'guide')
        #     return intent, 1.0

        if intent is not None:

            if '내일모레' in input_text or '모레' in input_text:
                intent = intent + '_day_after_tomorrow'
                return intent, 1.0
            elif '내일' in input_text:
                intent = intent + '_tomorrow'
                return intent, 1.0

            unused_words = ['오늘', '지금', '현재', '내일', '내일모레', '모레', '지역', '지방'] + list(reversed(list(self.dict_province2city.keys())))
            for _id, _city in self.dict_city2location.items():
                unused_words.append(_city['city'])

            for unused_word in unused_words:
                input_text = input_text.replace(unused_word, '')

            # input_text = input_text.replace(keyword, '')

            for sample in self.dict_intents[intent]:
                _s = sample.replace(' ', '')
                _confidence = self.compare_statements(input_text, _s)
                if _confidence > 0.8:
                    return intent, _confidence

        return None, 0.0


    def get_weather_info(self, input_text, remote_addr, statement):

        target_date = '오늘'
        target_city, target_city_loc = self.get_loc(input_text, remote_addr, statement)
        if target_city == ''and target_city_loc is None:return''

        # 좌표로 날씨 정보 가져오기
        url = 'https://api.openweathermap.org/data/2.5/weather?lat=' + str(target_city_loc['lat']) + '&lon=' + str(target_city_loc['lon']) + '&appid=' + self.OPENWEATHERMAP_APPID
        data_weather = requests.get(url)
        json_weather = json.loads(data_weather.content)

        response_text = self.dict_code2response[json_weather['weather'][0]['description']] % (target_date, target_city, )

        return response_text


    def get_loc(self, input_text, remote_addr, statement):
        target_city_str = ''

        print('1. %%%%%%%%%%% ----- get_loc', input_text)


        # 텍스트 기반 원하는 위치가 있는지 검사
        target_province = None
        target_city_loc = None

        arr_target_city_candidate = None

        # if statement.get_chatbot_id() == '4':
        #     target_city_str = '청도'
        #     target_city_loc = {
        #         "lat": 35.6472706,
        #         "lon": 128.7339107
        #     }

        for _province, _arr_city_candidate in self.dict_province2city.items():
            if _province in input_text:
                arr_target_city_candidate = _arr_city_candidate
                target_province = _province

        if arr_target_city_candidate is None:
            arr_target_city_candidate = self.dict_city2location.keys()

        for _city_id in arr_target_city_candidate:
            _city = self.dict_city2location[_city_id]
            print('2. %%%%%%%%%%% ----- get_loc', input_text, _city['city'])
            if _city['city'] in input_text:
                target_city_str = _city['city']
                target_city_loc = {
                    'lat': _city['lat'],
                    'lon': _city['lon']
                }
                break

        if target_city_loc is None and target_province is not None:
            _city = self.dict_city2location[response_selection.get_random_response(response_list=arr_target_city_candidate)]
            target_city_str = target_province + '지역'
            target_city_loc = {
                'lat': _city['lat'],
                'lon': _city['lon']
            }
        print('4. %%%%%%%%%%% ----- get_loc', target_city_loc)
        # 없으면 현재 위치 좌표의 가장 가까운 도시 좌표 가져오기

        print('chatbot_id : {}'.format(statement.chatbot.chatbot_id))
        return target_city_str, target_city_loc
        if target_city_loc is None:
            if statement.chatbot.chatbot_id == '4':
                print('chatbot_id type : {}'.format(type(statement.chatbot.chatbot_id)))
                target_city_str = '청도'
                target_city_loc = {
                    "lat": 35.6472706,
                    "lon": 128.7339107
                }
            elif statement.chatbot.chatbot_id == '20':
                target_city_str = '인천'
                target_city_loc={
                    "lat":37.4537645,
                    "lon":126.6865792
                }
            elif statement.chatbot.chatbot_id == '17':
                target_city_str = '광주'
                target_city_loc = {
                    "lat": 35.152332,
                    "lon": 126.838734
                }
            elif statement.chatbot.chatbot_id == '18':
                target_city_str = '유성구'
                target_city_loc={
                    "lat": 36.3818647,
                    "lon": 127.1930926
                }
            elif statement.chatbot.chatbot_id == '19':
                target_city_str = '진주시'
                target_city_loc = {
                    "lat": 35.1823151,
                    "lon": 128.0548305
                }
            else:
                target_city_str = '울산'
                target_city_loc = {
                    "lat": 35.5445793,
                    "lon": 129.2526532
                }

            # data_iploc = requests.get('http://ip-api.com/json/' + remote_addr)
            # json_iploc = data_iploc.json()
            # try:
            #     _lat = json_iploc['lat']
            #     _lon = json_iploc['lat']
            #
            #     deviation = 1000
            #     city_id = -1
            #
            #     for _city_id, _city in self.dict_city2location.items():
            #         _deviation = (abs(_lat - _city['lat']) + abs(_lon - _city['lon'])) / 2
            #         if deviation > _deviation:
            #             deviation = _deviation
            #             city_id = _city_id
            #
            #     _city = self.dict_city2location[city_id]
            #     target_city_str = _city['city']
            #     target_city_loc = {
            #         'lat': _city['lat'],
            #         'lon': _city['lon']
            #     }
            #
            # except Exception as e:
            #     print(e)
            #     pass

        # 그래도 안구해지면 대표 좌표로 대체
        if target_city_loc is None:
            _city = self.dict_city2location['0']
            target_city_str = '서울 기준'
            target_city_loc = {
                'lat': _city['lat'],
                'lon': _city['lon']
            }

        return target_city_str, target_city_loc


