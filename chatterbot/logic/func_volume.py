from chatterbot.logic import LogicAdapter
from chatterbot import response_selection

from chatterbot import utils

import json


class FuncVolumeAdapter(LogicAdapter):

    DICT_PATH = "chatterbot/logic/func_volume/"

    dict_intents = json.load(open(DICT_PATH+"intents.json"))
    dict_intents_keywords = json.load(open(DICT_PATH+"intents_keyword.json"))
    dict_intents_verb = json.load(open(DICT_PATH+"intents_verb.json"))
    dict_response = json.load(open(DICT_PATH+"response.json"))


    def can_process(self, statement):
        return True

    def process(self, statement):

        intent, confidence = self.recognize_intent(statement)

        if intent == "guide_volume_ctrl":
            _text = response_selection.get_random_response(response_list=self.dict_response[intent])
            statement.set_output(_text, 'FuncVolume', intent, confidence)

        elif intent == "request_volume_up":
            _text = response_selection.get_random_response(response_list=self.dict_response[intent])
            statement.set_output(_text, 'FuncVolume', intent, confidence)
            statement.set_output_cmd('volume_up')

        elif intent == "request_volume_down":
            _text = response_selection.get_random_response(response_list=self.dict_response[intent])
            statement.set_output(_text, 'FuncVolume', intent, confidence)
            statement.set_output_cmd('volume_down')

        return statement



    def recognize_intent(self, statement):
        input_text = statement.input['text'].replace(' ', '')

        intent = None
        intent_for_keyword = None

        for _intent, _samples in self.dict_intents.items():
            for sample in _samples:
                _confidence = self.compare_statements(input_text, sample.replace(' ', ''))
                if _confidence > 0.8:
                    return _intent, _confidence

        if intent is None:
            for _intent, _samples in self.dict_intents_verb.items():
                for sample in _samples:
                    if sample.replace(' ', '') in input_text:
                        intent = _intent
                        break
                if intent is not None:
                    break

        if intent is not None:
            for _intent, _samples in self.dict_intents_keywords.items():
                for sample in _samples:
                    if sample in input_text:
                        intent_for_keyword = _intent

            if intent_for_keyword == 'request_volume' and intent == 'request_volume_up':
                return 'request_volume_up', 1.0
            elif intent_for_keyword == 'request_volume' and intent == 'request_volume_down':
                return 'request_volume_down', 1.0
            elif intent_for_keyword == 'request_volume':
                return 'guide_volume_ctrl', 1.0

        return None, 0.0








