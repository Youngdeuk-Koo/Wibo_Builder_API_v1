from chatterbot.state.LonelyDeathState import LDeathMsgStateFlow
from chatterbot.logic.preception_lonely_death_modules.SurveyModel import QuestionSelectModel, SurveyEvaluationModel
from chatterbot.logic.preception_lonely_death_modules.SelectionQuestionIndex import QuestionIndexSelectModel



class SurveyFlowEngine() :

    def __init__(self, db, cache, user_key):
        self.db = db
        self.cache = cache
        self.user_key = user_key

        self.questionIndexSelectModel = QuestionIndexSelectModel(self.db, self.user_key)
        self.stateMachine = LDeathMsgStateFlow(self.cache.storage, self.user_key, self.db)

        self.questionSelectModel = QuestionSelectModel(self.cache.storage)
        self.surveyEvaluationModel = SurveyEvaluationModel()

    def start_process(self, text):

        last_intent = self.cache.get_intent(self.user_key)

        if last_intent is None or "고독사_" not in last_intent:


            msg_index = self.stateMachine.get_pre_index()

            if msg_index is None:
                msg_index = self.questionIndexSelectModel.select(self.user_key)

            print("msg_index : ", msg_index)

            if msg_index is not None:
                self.stateMachine.start(msg_index)

                feature = self.surveyEvaluationModel.evaluation(self.stateMachine.state, text)

                next_state = self.stateMachine.next_state(feature)

                self.stateMachine.transition(next_state)
                self.stateMachine.save_state()
                answer = self.questionSelectModel.select(self.stateMachine.state, self.user_key)
                intent_title = "고독사_" + self.stateMachine.state

                return answer, intent_title

        return None, None

    def check_process(self, text):

        pre_state = self.stateMachine.get_pre_state()
        pre_index = self.stateMachine.get_pre_index()

        print(" ==> pre_index", pre_index)

        last_intent = self.cache.get_intent(self.user_key)

        if pre_index is not None and \
                (pre_state is not None or last_intent is None or "고독사_" not in last_intent):

            self.stateMachine.start(pre_index)

            feature = self.surveyEvaluationModel.evaluation(self.stateMachine.state, text)
            next_state = self.stateMachine.next_state(feature)
            print("next_state 1: ", self.stateMachine.state)

            if next_state is not None and not self.stateMachine.is_depth_line and "고독사_" in last_intent:
                self.stateMachine.transition(next_state)
                self.stateMachine.save_state()
                question = self.questionSelectModel.select(self.stateMachine.state, self.user_key)
                print("next_state 2 : ", self.stateMachine.state)

                return question, self.stateMachine.state

        return None, None
