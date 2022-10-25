from chatterbot.logic import CustomAdapter
from chatterbot.functions import make_response
from chatterbot import response_selection

from random import choice
import requests, json

class AirPollutionAdapter(CustomAdapter):

    DATAGOKR_APPID = "q5d86gX8pheW0VQUemaVxZjmpDQjrxmDDTWgTwiN4UDUT1Xw6N2utWd06ZZEYIiPTosJGLxTlBSDLC0x4RHLaA%3D%3D"

    DICT_PATH = "chatterbot/logic/air_pollution/"
    dict_intents_cmd = json.load(open(DICT_PATH + "intents_cmd.json"))
    dict_intents = json.load(open(DICT_PATH + "intents.json"))
    dict_intents_keyword = json.load(open(DICT_PATH + "intents_keyword.json"))
    dict_response = json.load(open(DICT_PATH + "response.json"))
    dict_code2response = json.load(open(DICT_PATH + "code2response.json"))
    dict_province2city = json.load(open(DICT_PATH + "province2city.json"))
    dict_city2location = json.load(open(DICT_PATH + "city2location.json"))
    dict_province2rep_province = json.load(open(DICT_PATH + "province2rep_province.json"))

    def can_process(self, statement):
        return True

    def process(self, statement, intent=None):

        if intent is None:
            intent, confidence = self.recognize_intent(statement)
        else:
            confidence = 1.0

        if intent is not None:
            input_text = statement.input['text']
            if intent in ("request_air_pollution"):
                remote_addr = statement.request.get('remote_addr', None)
                statement.context['variables'].update(self.get_air_pollution_info(input_text, remote_addr))
                intent = intent + '_' + statement.context['variables']['air_pollution_degree']

            intentnode_id = self.chatbot.storage.get_custom_intent_node_id_for_text(self.id, intent)
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


    def get_air_pollution_info(self, input_text, remote_addr):

        target_date = '오늘'

        target_city, target_province, target_str = self.get_loc(input_text, remote_addr)

        rep_province = choice(self.dict_province2rep_province[target_province])

        url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?sidoName=" \
              + rep_province + "&searchCondition=DAILY&pageNo=1&numOfRows=30&ServiceKey=" + self.DATAGOKR_APPID
        data_air_pollution = requests.get(url)


        import xmltodict
        dict_air_pollution = json.loads(json.dumps(xmltodict.parse(data_air_pollution.text)))

        dict_air_pollution_items = dict_air_pollution['response']['body']['items']['item']


        def get_p_degree_str(_value):
            if 30 >= _value:
                return '좋음', 'good'
            elif 80 >= _value:
                return '보통', 'normal'
            elif 150 >= _value:
                return '나쁨', 'bad'
            else:
                return '매우나쁨', 'verybad'

        def get_air_p_degree_avr(_arr):
            _date = None
            idx = 0
            sum_pm10Value = 0
            for _item in _arr:
                try:
                    if _date is None:
                        _date = _item['dataTime']

                    if _date != _item['dataTime']:
                        break
                    sum_pm10Value += int(_item['pm10Value'])
                    idx += 1
                except:
                    pass
            pm10Value = sum_pm10Value/idx
            return pm10Value

        def get_air_p_degree(_arr, _target_city):
            pm10Value = 0
            for _item in _arr:
                if _target_city in _item['cityName']:
                    pm10Value = _item['pm10Value']
                    break
            if pm10Value == 0:
                pm10Value = _arr[0]['pm10Value']

            if pm10Value == '-':
                for _item in _arr:
                    if str(_item['pm10Value']).isdigit():
                        pm10Value = _item['pm10Value']

            return int(pm10Value)


        if target_city in ['서울', '광주', '대구', '대전', '부산', '세종', '울산', '인천']:
            get_air_p_degree = get_air_p_degree_avr(dict_air_pollution_items)
            air_p_degree_str, air_p_degree_class = get_p_degree_str(get_air_p_degree)
        elif target_city is None:
            get_air_p_degree = get_air_p_degree_avr(dict_air_pollution_items)
            air_p_degree_str, air_p_degree_class = get_p_degree_str(get_air_p_degree)
        else:
            get_air_p_degree = get_air_p_degree(dict_air_pollution_items, target_city)
            air_p_degree_str, air_p_degree_class = get_p_degree_str(get_air_p_degree)

        response_text = choice(self.dict_code2response[air_p_degree_str]) % (target_str)

        return {
            'air_pollution_info': response_text,
            'target_date': target_date,
            'target_city': target_city,
            'air_pollution_degree': air_p_degree_class
        }


    def get_loc(self, input_text, remote_addr):
        target_str = None

        # 텍스트 기반 원하는 위치가 있는지 검사
        target_province = None
        target_city_id = None
        target_city = None

        arr_target_city_candidate = None

        for _province, _arr_city_candidate in self.dict_province2city.items():
            if _province in input_text:
                arr_target_city_candidate = _arr_city_candidate
                target_province = _province

        if arr_target_city_candidate is None:
            arr_target_city_candidate = self.dict_city2location.keys()

        for _city_id in arr_target_city_candidate:
            _city = self.dict_city2location[_city_id]
            if _city['city'] in input_text:
                target_str = _city['city']
                target_city = _city['city']
                target_city_id = _city_id
                break

        # if target_city is None and target_province is not None:
        #     target_str = target_province + '지역'
        #     target_city = target_province
        # elif target_city is not None:
        #     target_str = target_city + '지역'
        # else:
        #     # 없으면 현재 위치 좌표의 가장 가까운 도시 좌표 가져오기
        #     _city = self.dict_city2location["129"]
        #     target_str = _city['city']
        #     target_city = _city['city']
        #     target_city_id = "129"

            #
            #
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
            #     target_str = _city['city']
            #     target_city = _city['city']
            #     target_city_id = city_id
            #
            # except Exception as e:
            #     print(e)
            #     pass

        # 그래도 안구해지면 대표 좌표로 대체
        if target_str is None:
            _city = self.dict_city2location['0']
            target_str = _city['city'] + ' 기준'
            target_city = _city['city']
            target_province = _city['city']

        if target_province is None and target_city_id is not None:
            for _province, _arr_city_candidate in self.dict_province2city.items():
                if target_city_id in _arr_city_candidate:
                    target_province = _province
                    break

        return target_city, target_province, target_str

