from chatterbot.logic import LogicAdapter
from chatterbot import response_selection
from chatterbot.comparisons import levenshtein_distance

import json


class KnowledgeAdapter(LogicAdapter):

    DICT_PATH = "chatterbot/logic/knowledge/"

    dict_intents = json.load(open(DICT_PATH+"intents.json"))
    dict_entities = json.load(open(DICT_PATH+"entities.json"))
    dict_response = json.load(open(DICT_PATH+"response.json"))

    def can_process(self, statement):
        return True


    def process(self, statement, intent=None):
        if intent is None:
            intent, confidence = self.recognize_intent(statement)
        else:
            confidence = 1.0

        if intent == "request_knowledge":
            _user_key = statement.request['user_key']
            _key, _response = self.get_randum_knowledge()
            _text = self.random_cache_response(_user_key, 'knowledge', _key, _response)

            statement.output.append({"text": _text})
            statement.result['module'].insert(0, self.title)
            statement.result['intent'].insert(0, intent)
            statement.result['confidence'] = 1.0

        return statement


    def recognize_intent(self, statement):
        input_text = statement.input['text'].replace(' ', '')

        for _intent, _samples in self.dict_intents.items():
            for sample in _samples:
                _confidence = self.compare_statements(input_text, sample.replace(' ', ''))
                if _confidence > 0.8:
                    return _intent, _confidence

        return None, 0.0



    def recognize_entity(self, input_text):
        def window(fseq, window_size=5):
            for i in range(len(fseq) - window_size + 1):
                start = i
                end = i + window_size
                yield fseq[start:end]

        for _entity_title, _entity_items in self.dict_entities.items():
            for _item in _entity_items:
                _tmp_item = _item.replace(' ', '')
                for _seq in window(input_text, len(_tmp_item)):
                    _confidence = levenshtein_distance(_tmp_item, _seq)
                    if _confidence > 0.8:
                        return input_text.replace(_seq, '@' + _entity_title)
        return input_text

    def get_randum_knowledge(self):
        _keys = self.dict_response.keys()
        _key = response_selection.get_random_response(response_list=list(_keys))
        return _key, self.dict_response[_key]