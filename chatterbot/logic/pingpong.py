#-*- coding: utf-8 -*-
from chatterbot.logic import LogicAdapter
from chatterbot import response_selection
from chatterbot.comparisons import levenshtein_distance
from chatterbot import utils
import logging
import json
import random, requests, re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

cnt = 0
class PingPongAdapter(LogicAdapter):

    def can_process(self, statement):
        return True

    def process(self, statement, intent=None):

        
        if intent == "request_pingpong":

            input_text = statement.input['text']
            
            try:    
                # URL = 'http://34.64.190.233:10734/chatbot/' + input_text
                URL = 'http://34.64.190.233:10734/chatbot/g?s=' + input_text
                data= requests.get(URL)
                j_data = json.loads(data.content)
                output = j_data["answer"]
                output = re.sub('[^a-z A-Z 가-힣 0-9 .,?!_]', '', output)

                statement.result['logic_property'] = 'koochat_logic'
                statement.result['module'] = ['KooChat']
                statement.result['intent'] = ['request_koochat']

            except:
                logging.info('Server Error')

                output_list = [
                    "다시 한번 말씀해주시겠어요?",
                    "죄송해요 못알아 들었어요 다시 말씀해주세요",
                    "제가 요즘 아파서 귀가 잘안들려요 조금 기다렸다 다시 말씀해주실래요?",
                    "어르신 죄송해요 못알아 들었어요 한번 더 말씀해주세요",
                    ]

                output = random.choice(output_list)
                statement.result['logic_property'] = 'server_error'
                statement.result['module'] = ['Emergency_Chat']
                statement.result['intent'] = 'request_emergency'
                

            statement.output.append({"text": output})
                     
            utils.log_write('koochat', statement) 

        return statement

