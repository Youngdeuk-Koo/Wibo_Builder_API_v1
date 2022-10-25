from chatterbot.logic import LogicAdapter
from chatterbot import response_selection
from chatterbot.utils import replace_entity


class SurveyAdapter(LogicAdapter):

    def can_process(self, statement):
        return True

    def process(self, statement):
        # check context

        # if first:
        # generate quiz message

        # if waiting status for answer:
        # recognize intent

        return statement



