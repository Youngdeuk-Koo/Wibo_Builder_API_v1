from chatterbot.logic import LogicAdapter
from chatterbot import response_selection

import json, copy

class LifeManagerAdapter(LogicAdapter):

    DICT_PATH = "chatterbot/logic/life_manager/"
    dict_intents = json.load(open(DICT_PATH+"intents.json"))
    dict_cards = json.load(open(DICT_PATH+"cards.json"))
    dict_response = json.load(open(DICT_PATH+"response.json"))


    def can_process(self, statement):
        return True

    def process(self, statement, intent=None):

        # 의도 분석
        user_key = statement.request['user_key']
        card_key = self.get_card_key(statement)

        if intent is None:
            intent, confidence = self.recognize_intent(statement)
        else:
            confidence = 1.0

        if card_key is not None:
            if intent == 'answer_pos':
                _card = self.dict_cards[card_key]
                _text = response_selection.get_random_response(response_list=self.dict_response['answer_pos']) \
                        + " " + response_selection.get_random_response(response_list=_card['answer_pos'])

                statement.output.append({"text": _text})
                statement.result['module'].insert(0, self.title)
                statement.result['intent'].insert(0, intent)
                statement.result['confidence'] = 1.0

                del statement.context['life_manager']
                self.chatbot.storage.save_user_life_state(user_key, card_key, 1)


            elif intent == 'answer_neg':
                _card = self.dict_cards[card_key]
                _text = response_selection.get_random_response(response_list=self.dict_response['answer_neg']) \
                        + " " + response_selection.get_random_response(response_list=_card['answer_neg'])

                statement.output.append({"text": _text})
                statement.result['module'].insert(0, self.title)
                statement.result['intent'].insert(0, intent)
                statement.result['confidence'] = 1.0

                del statement.context['life_manager']
                self.chatbot.storage.save_user_life_state(user_key, card_key, 0)

            else:
                if statement.context['life_manager']['answer_count'] < 1:
                    _text = response_selection.get_random_response(response_list=self.dict_response['answer_else'])

                    statement.output.append({"text": _text})
                    statement.result['module'].insert(0, self.title)
                    statement.result['intent'].insert(0, "answer_else")
                    statement.result['confidence'] = 1.0

                    statement.context['life_manager']['answer_count'] += 1
                else:
                    del statement.context['life_manager']

        elif intent == 'request_life_manage':
            statement = self.get_initial_message(statement)

            _dict_cards = self.get_cards()

            _dict_user_state = self.chatbot.storage.get_user_life_state(user_key, _dict_cards.keys())

            dict_cards = copy.deepcopy(_dict_cards)
            for _key in _dict_cards.keys():
                if _key in _dict_user_state.keys():
                    if _dict_user_state[_key] == 1:
                        del dict_cards[_key]
                        continue
                    else:
                        dict_cards[_key]['state'] = _dict_user_state[_key]
                dict_cards[_key]['state'] = None

            if len(dict_cards.keys()) > 0:
                _card_key = response_selection.get_random_response(response_list=list(dict_cards.keys()))

                _card = dict_cards[_card_key]
                _text = response_selection.get_random_response(response_list=_card['question'])

                statement.output.append({"text": _text})
                statement.result['module'].insert(0, self.title)
                statement.result['intent'].insert(0, intent)
                statement.result['confidence'] = 1.0
                statement.context['life_manager']['card_key'] = _card_key

        return statement


    def get_initial_message(self, statement):
        if 'life_manager' not in statement.context:
            statement.context['life_manager'] = {
                'card_key': -1,
                'answer_count': 0
            }
        return statement


    def get_card_key(self, statement):
        if 'life_manager' in statement.context:
            if statement.context['life_manager']['card_key'] != -1:
                return statement.context['life_manager']['card_key']
        return None


    def recognize_intent(self, statement):
        input_text = statement.input['text'].replace(' ', '')

        for _intent, _samples in self.dict_intents.items():
            for sample in _samples:
                _confidence = self.compare_statements(input_text, sample.replace(' ', ''))
                if _confidence > 0.8:
                    return _intent, _confidence

        return None, 0.0


    def get_cards(self):
        from datetime import datetime
        now = datetime.now()

        slots = {}
        for slot_key, slot in self.dict_cards.items():
            if now.hour in slot['time']:
                slots[slot_key] = slot

        return slots
        # return self.dict_cards
