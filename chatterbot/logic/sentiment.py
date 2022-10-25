from chatterbot.logic import CustomAdapter

from chatterbot.logic.sentiment_modules.sentiment_step1 import SentimentStep1
from chatterbot.logic.sentiment_modules.reaction_step1 import ReactionStep1
from chatterbot.logic.util.output_by_db import OutputByDB
from konlpy.tag import Mecab


class SentimentAdapter(CustomAdapter):


    def can_process(self, statement):
        """
        Check that the chatbot's storage adapter is available to the logic
        adapter and there is at least one statement in the database.
        """
        return True
        # return self.chatbot.storage.has_chatbot(statement.chatbot_id)

    def process(self, input_statement):

        return self.get_chat_response(input_statement)


    def get_chat_response(self, statement):

        mecab = Mecab()
        # DB = OutputByDB()
        sentimentStep1 = SentimentStep1(mecab, "/home/wiboe/data" )
        # reactionStep1 = ReactionStep1(mecab, DB)
        category, response  = sentimentStep1.get_chat_response(statement)
        intents = self.get_intents()


        if response is not None :
            response_text = self.select_response(response_list=intents[response]["output"].split(","))

            statement.set_output(
                _text=response_text,
                _module='',
                _intent=response,
                _confidence=1.0
            )

            return statement

        # if statement.output['confidence'] == 0.0 :
        #     DB = OutputByDB()
        #     reactionStep1 = ReactionStep1(mecab, DB, "/home/wiboe/data")
        #     statement = reactionStep1.get_chat_response(input_statement)
        #     DB.close()

        statement.set_output(
            _text='',
            _module='',
            _intent="감정대화",
            _confidence= 0.0
        )

        return statement


