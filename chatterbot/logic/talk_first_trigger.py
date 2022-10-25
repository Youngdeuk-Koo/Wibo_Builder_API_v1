from chatterbot.logic import LogicAdapter
from chatterbot.functions import make_response

from random import choice
import json


class TalkFirstTriggerAdapter(LogicAdapter):

    DICT_PATH = "chatterbot/logic/talk_first_trigger/"
    dict_intents = json.load(open(DICT_PATH+"intents.json"))
    dict_response = json.load(open(DICT_PATH+"response.json"))
    


    def can_process(self, statement):
        return True

    def process(self, statement, intent=None):
        if intent is None:
            intent, confidence = self.recognize_intent(statement)
        else:
            confidence = 1.0

        if intent == 'talk_first':
            statement = self.get_initial_message(statement)
            import datetime as pydatetime
            now = pydatetime.datetime.now()
            statement.context['talk_first']['updated_time'] = now.timestamp()

            _text = choice(self.dict_response['talk_first'])
            statement.output.append({"text": _text})
            statement.result['module'].insert(0, self.title)
            statement.result['intent'].insert(0, intent)
            statement.result['confidence'] = 1.0

            return statement

        if 'talk_first' in statement.context:
            # if not self.is_overtime(statement.context['talk_first']['updated_time']):
            #     intent = "talk_first_reaction"
            #     intentnode_id = self.chatbot.storage.get_custom_intent_node_id_for_text(self.id, intent)
            #     if intentnode_id is not None:
            #         response_groups = self.chatbot.storage.get_custom_response_groups(intentnode_id)
            #         response_group = choice(response_groups)
            #         for response in response_group['data']:
            #             statement = make_response(response, statement)
            #     else:
            #         _text = choice(self.dict_response[intent])
            #         for _key, _value in statement.context['variables'].items():
            #             _text = _text.replace('{' + _key + '}', _value)
            #         statement.output.append({"text": _text})
            #
            #     statement.result['module'].insert(0, self.title)
            #     statement.result['intent'].insert(0, intent)
            #     statement.result['confidence'] = 1.0

            del statement.context['talk_first']

        return statement


    def get_initial_message(self, statement):
        if 'talk_first' not in statement.context:
            statement.context['talk_first'] = {
                'updated_time': 0
            }
        return statement


    def recognize_intent(self, statement):
        input_text = statement.input['text']
        for _intent, _samples in self.dict_intents.items():
            for sample in _samples:
                _confidence = self.compare_statements(input_text, sample.replace(' ', ''))
                if _confidence > 0.8:
                    return _intent, _confidence
        return None, 0.0


    def is_overtime(self, pre_timestamp):
        from datetime import datetime
        pre_datetime_obj = datetime.fromtimestamp(pre_timestamp)
        now_obj = datetime.now()
        delta = now_obj - pre_datetime_obj
        if delta.seconds > 1:
            return True
        return False


