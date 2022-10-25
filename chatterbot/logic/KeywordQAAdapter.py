from chatterbot.logic import LogicAdapter
import pandas as pd

from konlpy.tag import Mecab


from chatterbot.logic.keyword_qa_modules.pattern_util import PatternUtil

from chatterbot.logic.keyword_qa_modules.response_util import ResponseUtil

from chatterbot.logic.keyword_qa_modules.faq_data_by_db import FAQDataDB

class KeywordQAAdapter(LogicAdapter):

    def can_process(self, statement):
        """
        Check that the chatbot's storage adapter is available to the logic
        adapter and there is at least one statement in the database.
        """
        return True
        # return self.chatbot.storage.has_chatbot(statement.chatbot_id)

    def process(self, input_statement):
        return self.get_chat_response(input_statement)

    def get_chat_response(self, input_statement):

        user_key = input_statement.request['user_key']


        # print (input_statement.serialize())
        #print ("macab: " , input_statement.input['_macab'])

        mecab = Mecab()

        patternUtil = PatternUtil(mecab)

        intents = patternUtil.check_intent_rule(input_statement.input['text'])

        conn, curs = self.chatbot.storage.get_resource()

        faqDataDB = FAQDataDB(conn, curs)

        responseUtil = ResponseUtil(input_statement.chatbot["id"], faqDataDB)
        response, title, category_name = responseUtil.check_response(self.id, intents, input_statement.input['text'])

        if response is not None and len(response) > 0 :
            intent = title + "," + category_name
            answer = self.random_cache_response(user_key, self.id, intent, response.split(','))

            input_statement.set_output(
                _text = answer,
                _module = '',
                _intent = intent,
                _confidence= 1.0
            )
            #input_statement.output['text'] = response
            #input_statement.output['confidence'] = 1.0
        else :
            input_statement.set_output(
                _text='',
                _module='',
                _intent='',
                _confidence= 0.0
            )
        return input_statement



