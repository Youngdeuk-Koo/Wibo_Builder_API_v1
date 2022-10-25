from chatterbot.logic import CustomAdapter
from chatterbot.logic.preception_lonely_death_modules.SurveyFlowEngine import  SurveyFlowEngine

class PreceptionLonelyDeath(CustomAdapter):


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

        user_key = statement.request['user_key']
        _, cur = self.chatbot.storage.get_resource()
        surveyFlowEngine = SurveyFlowEngine(cur, self.chatbot.cache_storage, user_key)
        question, state = surveyFlowEngine.check_process(statement.input['text'])

        if question is None :
            statement.set_output(
                _text="",
                _module="고독사유형감지",
                _intent="",
                _confidence=0.0
            )
        else :
            statement.set_output(
                _text= question,
                _module="고독사유형감지",
                _intent= "고독사_" + state,
                _confidence= 1.0
            )

        return statement


