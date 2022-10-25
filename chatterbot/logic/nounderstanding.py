#-*- coding: utf-8 -*-

from chatterbot.logic import LogicAdapter
from chatterbot.logic.preception_lonely_death_modules.SurveyFlowEngine import SurveyFlowEngine

from chatterbot import utils

import requests, json
import re

from random import choice


class NoUnderstandingAdapter(LogicAdapter):
    """
    A logic adapter that returns a response based on known responses to
    the closest matches to the input statement.
    """
    DICT_PATH = "chatterbot/logic/nounderstanding/"
    dict_add_response = json.load(open(DICT_PATH + "add_response.json"))

    def can_process(self, statement):
        return True


    def process(self, statement):

        # 그냥 무응답
        # 무응답
        is_program = choice([True, False])

        if is_program:

            adapters = []

            def set_program_adapter(adapter_path=''):
                Class = utils.import_module(adapter_path)
                _adapter = Class(self.chatbot)
                adapters.append(_adapter)

            set_program_adapter('chatterbot.logic.KnowledgeAdapter')
            set_program_adapter('chatterbot.logic.LifeManagerAdapter')

            adapter = choice(adapters)

            import copy
            _sta = copy.deepcopy(statement)
            _sta.input['text'] = "[knowledge]"
            _sta = adapter.process_add(_sta)

            intents = self.chatbot.storage.get_nounderstandings(self.id)
            intent = None
            for _intent in intents:
                if "module_switching" == _intent['title']:
                    intent = _intent
            if intent is None:
                intent = self.select_response(response_list=intents)
            response_text = self.select_response(response_list=intent['output'].split(',')).strip() + " " + self.select_response(response_list=self.dict_add_response["module_switching"]) + " " + _sta.output['text']
            _sta.set_output(_text=response_text, _module='', _intent=intent['title'], _confidence=1.0)
            statement = _sta

        else:
            user_key = statement.request['user_key']
            intents = self.chatbot.storage.get_nounderstandings(self.id)
            intent = self.select_response(response_list=intents)
            response_text = self.random_cache_response(user_key, self.id, intent['title'], intent['output'].split(','))
            statement.set_output(_text=response_text, _module='', _intent=intent['title'], _confidence=1.0)

        return statement

        # return self.get_else_response(input_statement)
















    def get_else_response(self, statement):
        text = statement.input['text']

        ## 핑퐁 부분
        # re_text = self.send_pingpong(text)
        # if re_text is not None :
        #     text = self.strip_e(re_text)
        #     statement.set_output(_text=text, _module='', _intent="못알아들음-api", _confidence=1.0)
        #     return statement

        ## 설문조사 진행 엔진
        user_key = statement.request['user_key']
        _, cur = self.chatbot.storage.get_resource()
        surveyFlowEngine = SurveyFlowEngine(cur, self.chatbot.cache_storage, user_key)
        _text = statement.input['text']

        answer, intent_title = surveyFlowEngine.start_process(text)


        ### 설문조사가 아니면 이해 못할때 말
        if answer is None :

            log_text = "캐시임"
            intent_title, answer = self.chatbot.cache_storage.nounderstanding(user_key)
            if intent_title is None :
                outputs = []
                intents = self.chatbot.storage.get_nounderstandings(self.id)
                for intent in intents :
                    outputs.append(intent['title'] + ":" + intent['output'])

                self.chatbot.cache_storage.nounderstanding_save(user_key, outputs)

                intent_title, answer = self.chatbot.cache_storage.nounderstanding(user_key)


                # intent = self.select_response(response_list=intents)
                # text = self.select_response(response_list=intent['output'].split(','))

                # intent_title = intent['title']
                # answer = text

                log_text = "캐시아님"

            # print("===>", log_text)



        statement.set_output(_text=answer, _module='', _intent=intent_title, _confidence=1.0)
        return statement

    def strip_e(self, st):
        RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
        return RE_EMOJI.sub(r'', st)

    def send_pingpong(self, text):
        headers = {'Content-Type': 'application/json', 'Authorization' :'Basic a2V5OmVlNmNkZTgzNDY3NzZlYzcwYmZjMDBiNTA2MjVkMjEz'}
        #res = requests.get("https://builder.pingpong.us/api/builder/5d566e1be4b03bd914d2fee7/integration/v0.2/custom/1234", headers=headers)
        data = {'request': {'query': text}}
        res = requests.post("https://builder.pingpong.us/api/builder/5d566e1be4b03bd914d2fee7/integration/v0.2/custom/1234",headers=headers, data=json.dumps(data))
        response = res.json()
        if "replies" in response["response"] :
            replies = response["response"]["replies"]

            for reply in replies :
                if reply["type"] == "text" :
                    re_text = reply["text"].replace("핑퐁", "돌돌이")
                    re_text = re_text.replace("pingpong", "돌돌이")
                    re_text = re_text.replace("스캐터랩", "미스터마인드")
                    return re_text
        return None
