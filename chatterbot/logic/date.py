from chatterbot.logic import CustomAdapter
from chatterbot.functions import make_logic_response

from random import choice
import json

class DateAdapter(CustomAdapter):

    DICT_PATH = "chatterbot/logic/date/"
    dict_response = json.load(open(DICT_PATH + "response.json"))

    def can_process(self, statement):
        return True

    def process(self, statement, intent=None):
        
        logic_name = "date_logic"

        date_response, intent = self.get_date(statement)

        response = ''.join(self.dict_response[intent])

        for _key, _val in date_response.items():
            response = response.replace('{' + _key + '}', _val)
            # statement.output.append({"text": response})

        statement = make_logic_response(response, logic_name, statement)

        # statement.result['intent_id'] = 0
        statement.result['module'].insert(0, self.title)
        # statement.result['chatbot_id'] = self.chatbot_id

        return statement


    def get_date(self, statement):

        timedelta_day = 0

        yesterday_text = ['어제', '어제가', '어제는', '지난날']
        today_text = ['오늘', '지금', '지금이']
        tomorrow_text = ['내일', '내일은', '내일이', '다음날', '다음날이']
        after_tomorrow_text = ['내일모레', '내일모레는', '모레', '모레가', '모레는', '이틀', '다다음날', '다다음']

        sentence = statement.input['text'].split()

        bul = False

        for text in sentence:
            if text in yesterday_text:
                timedelta_day = -1
                _target = '어제는'
                bul = True
                break
            
            elif text in today_text:
                timedelta_day = 0
                _target = '오늘은'
                bul = True
                break

            elif text in tomorrow_text:
                
                if '모레' in sentence:
                    timedelta_day = 2
                    _target = '내일 모레는'
                    bul = True
                    break

                else:
                    timedelta_day = 1
                    _target = '내일은'
                    bul = True
                    break

            elif text in after_tomorrow_text:
                timedelta_day = 2
                _target = '내일 모레는'
                bul = True

            else:
                continue
        
        if bul == False:
            timedelta_day = 0
            _target = '오늘은'


        from datetime import date, timedelta

        _date = date.today() + timedelta(timedelta_day)

        t = ['월', '화', '수', '목', '금', '토', '일']

        return {
            'target': _target,
            'year': str(_date.year),
            'month': str(_date.month),
            'day': str(_date.day),
            'weekday': t[_date.weekday()],
        }, 'request_date'


