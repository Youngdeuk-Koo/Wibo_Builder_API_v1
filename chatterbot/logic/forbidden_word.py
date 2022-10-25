from chatterbot.logic import LogicAdapter
from chatterbot import response_selection


class ForbiddenWordAdapter(LogicAdapter):

    def can_process(self, statement):
        return True


    def process(self, input_statement):
        return self.get_response(input_statement)

 

    def get_response(self, statement):
        intents = self.chatbot.storage.get_forbiddenwords(self.id)

        is_matched = False

        for intent in intents:
            for word in intent['input'].split(','):
                word = word.strip()
                if word != '' and word in statement.input['text'].strip():
                    print(word.strip(), statement.input['text'].strip())
                    text = self.select_response(response_list=intent['output'].split(','))
                    statement.set_output(_text=text, _module='', _intent=intent['title'], _confidence=1.0)
                    is_matched = True
                    break
            if is_matched:
                break

        return statement



