from chatterbot.logic import LogicAdapter
from chatterbot.functions import make_logic_response


class MusicAdapter(LogicAdapter):

    def can_process(self, statement):
        return True

    def process(self, statement):

        logic_name='music_logic'
        response='request_music'

        input_text = statement.input['text']

        if self.chatbot_id == '8':

            if '노래' in input_text and '동요' not in input_text :
                statement.result['intent_id'] = 84

            elif '동요' in input_text or '클래식' in input_text:
                statement.result['intent_id'] = 67

            elif '노래' in input_text and '동요' in input_text:
                    statement.result['intent_id'] = 67

            else:
                statement.result['intent_id'] = 84


        elif self.chatbot_id == '20':

            if '노래' in input_text and '트로트' not in input_text:
                statement.result['intent_id'] = 67

            elif '트로트' in input_text:
                statement.result['intent_id'] = 84

            elif '노래' in input_text and '트로트' in input_text:
                    statement.result['intent_id'] = 84

            else:
                statement.result['intent_id'] = 67

        statement = make_logic_response(response, logic_name, statement)

        return statement