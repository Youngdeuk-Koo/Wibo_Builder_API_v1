#-*- coding: utf-8 -*-
from chatterbot.logic import LogicAdapter
from chatterbot import response_selection
from chatterbot.comparisons import levenshtein_distance

import json, requests

class PingPongAdapter(LogicAdapter):

    def can_process(self, statement):
        return True

    def process(self, statement, intent=None):

        if intent == "request_pingpong":
            input_text = statement.input['text']
            try:
                re_text = self.send_pingpong(input_text)
                if re_text is not None:
                    _text = self.strip_e(re_text)
                    statement.output.append({"text": _text})
                    statement.result['module'].insert(0, self.title)
                    statement.result['intent'].insert(0, intent)
                    statement.result['confidence'] = 1.0
            except:
                pass

        return statement

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

    def strip_e(self, st):
        import re
        RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
        st = RE_EMOJI.sub('', st)
        st = re.sub(r'\([^)]*\)', '', st)
        return st