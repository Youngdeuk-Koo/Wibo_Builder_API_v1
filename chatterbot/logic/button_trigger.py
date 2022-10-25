from chatterbot.logic import LogicAdapter
from chatterbot import response_selection

from chatterbot import utils

import json


class ButtonTriggerAdapter(LogicAdapter):

    DICT_PATH = "chatterbot/logic/button_trigger/"

    dict_intents = json.load(open(DICT_PATH+"intents.json"))

    def can_process(self, statement):
        return True

    def process(self, statement):

        intent, confidence = self.recognize_intent(statement)

        adapters = []
        def set_program_adapter(adapter_path=''):
            Class = utils.import_module(adapter_path)
            _adapter = Class(self.chatbot)
            adapters.append(_adapter)

        if intent == 'onclk_music':
            set_program_adapter('chatterbot.logic.MusicAdapter')
        elif intent == 'onclk_knowledge':
            set_program_adapter('chatterbot.logic.KnowledgeAdapter')
        elif intent == 'onclk_quiz':
            set_program_adapter('chatterbot.logic.OXQuizAdapter')

        if intent is not None:
            from random import choice
            adapter = choice(adapters)
            statement = adapter.process(statement)

        return statement


    def recognize_intent(self, statement):
        input_text = statement.input['text'].replace(' ', '')

        for _intent, _samples in self.dict_intents.items():
            for sample in _samples:
                _confidence = self.compare_statements(input_text, sample.replace(' ', ''))
                if _confidence > 0.95:
                    return _intent, _confidence

        return None, 0.0








