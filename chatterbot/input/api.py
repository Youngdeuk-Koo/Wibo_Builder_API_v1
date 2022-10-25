from chatterbot.input import InputAdapter
from chatterbot.conversation import Statement

from chatterbot import response_selection

class APIAdapter(InputAdapter):
    DICT = 'json'
    VALID_FORMATS = (DICT,)

    def process_input(self, statement):
        input_type = self.detect_type(statement)

        if input_type == self.DICT:

            statement = Statement(self.chatbot, **statement)
            if statement.is_timeover():
                statement.init_context()

            return statement

        return None



