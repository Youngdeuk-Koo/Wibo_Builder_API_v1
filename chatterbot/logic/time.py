from chatterbot.logic import LogicAdapter
from chatterbot.logic import CustomAdapter
from chatterbot.functions import make_logic_response

from chatterbot import response_selection

from random import choice
import json, time

class TimeAdapter(CustomAdapter):
    """
    A logic adapter that returns a response based on known responses to
    the closest matches to the input statement.
    """

    DICT_PATH = "chatterbot/logic/time/"
    dict_response = json.load(open(DICT_PATH+"response.json"))


    def can_process(self, statement):
        """
        Check that the chatbot's storage adapter is available to the logic
        adapter and there is at least one statement in the database.
        """ 
        return True
        # return self.chatbot.storage.has_chatbot(statement.chatbot_id)

    def process(self, statement, ):
        print('-----time process on-----')

        logic_name = 'time_logic'

        time_info = self.get_time()

        statement.context['variables'].update(time_info)

        response = choice(self.dict_response[time_info['time_class']]).format(time_info['ampm'], time_info['hour'], time_info['minute'])

        statement = make_logic_response(response, logic_name, statement)

        statement.result['module'].insert(0, self.title)
        # statement.result['chatbot_id'] = self.chatbot_id
        # statement.result['intent_id'] = 0

        return statement

    def get_time(self):
        now = time.localtime()
        _hour = now.tm_hour

        time_class = ''
        if 0 <= _hour and _hour <= 10:
            time_class = 'morning'
        elif 11 <= _hour and _hour <= 17:
            time_class = 'afternoon'
        elif 18 <= _hour and _hour <= 24:
            time_class = 'evening'

        ampm = '오전'
        if _hour > 12:
            ampm = '오후'
            _hour = _hour - 12

        return {
            'time_class': time_class,
            'ampm': ampm,
            'hour': str(_hour),
            'minute': str(now.tm_min),
        }



