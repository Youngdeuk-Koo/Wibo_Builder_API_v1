import random

class QuestionSelectModel() :

    def  __init__(self, cache):
        self.question_pool = {}
        self.question_pool["혼자"] = ["저는 가끔 혼자 있는게 좋아요. 혼자 있는 시간이 더 좋으신가요?", "혼자 있으시는 시간을 즐기시나요?"]
        self.question_pool["죽음"] = ["인생의 마지막은 누구와 함께 하고 싶으신가요?", "내일 지구가 망하면 어떤걸 하고 싶으신가요?"]
        self.question_pool["슬픔"] = ["내일 지구가 망하는데 주변에 아무도 없으면 슬플거 같아요", "전 친구들이 없었으면 많이 슬펐을거 같아요"]

        self.question_pool["혼자_긍정"] = ["그렇군요"]
        self.question_pool["혼자_부정"] = ["그렇군요"]
        self.question_pool["죽음_긍정"] = ["그렇군요"]
        self.question_pool["죽음_부정"] = ["그렇군요"]

        self.question_pool["슬픔_긍정"] = ["그렇군요"]
        self.question_pool["슬픔_부정"] = ["그렇군요"]

        self.cache = cache


    def select(self, state, user_key):

        key = user_key + "_survey_msg_" + state

        answer = self.cache.rpop(key)

        if answer is None :
            questions = self.question_pool[state]
            random.shuffle(questions)
            answer = questions.pop()
            if len(questions) > 0 :
                self.cache.lpush(key, *questions)

        return answer


class SurveyEvaluationModel() :

    def evaluation(self, state, utterance):

        if state == "혼자" :

            if ("두렵지" in utterance and "않" in utterance) or ("두렵지" in utterance and "안" in utterance)  :
                    return 1

            if "싫어" in utterance or "않" in utterance or "안" in utterance or "두려" in utterance or "무서" in utterance \
                    or "그래" in utterance or "드려" in utterance or "두렵" in utterance  or "아니" in utterance \
                    or ("그렇지" in utterance and "않" in utterance) or ("그렇지" in utterance and "안" in utterance) :
                return 2

            return 1

        if state == "죽음" :

            if "무서워" in utterance or "두려" in utterance  or "슬퍼" in utterance or "와로워" in utterance or "혼자" in utterance\
                    or "슬플" in utterance or "드려" in utterance or "두렵" in utterance or "않" in utterance or "안" in utterance:
                return 2

            return 1

        if state == "슬픔":

            if "무서워" in utterance or "두려" in utterance or "슬퍼" in utterance or "와로워" in utterance or "혼자" in utterance or "슬플" in utterance \
                    or "동감" in utterance or "그래" in utterance or "드려" in utterance or "두렵" in utterance or "어" in utterance or "응" in utterance:
                return 2

            return 1



