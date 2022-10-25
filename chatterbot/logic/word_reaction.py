from chatterbot.logic import LogicAdapter
from konlpy.tag import Mecab

wr_morph = Mecab()

class WordReaction(LogicAdapter):
    """
    A logic adapter that returns a response based on known responses to
    the closest matches to the input statement.
    """

    def can_process(self, statement):
        """
        Check that the chatbot's storage adapter is available to the logic
        adapter and there is at least one statement in the database.
        """
        return True
        # return self.chatbot.storage.has_chatbot(statement.chatbot_id)

    def process(self, input_statement):

        if input_statement.is_first:
            return self.get_init_response(input_statement)
        else:
            return self.get_chat_response(input_statement)


    def check_last_word(self, poss):


        if poss is None or len(poss) == 0 :
            return None
        last_word = poss[len(poss) - 1][0]



        if len(poss) < 2 :

            if last_word == "그래요":
                return "알았어요"

            if last_word == "놀이":
                return "즐겁겠네요"

            if last_word == "몰라":
                return "흠 그래요"

        else :
            front_word = poss[len(poss) -2][0]

            # print("reaction word => ", front_word, last_word)

            if poss[0][0] == "왜":
                return '저도 몰라요'

            if  last_word == "놀이":
                return "즐겁겠네요"


            if  last_word == "해요":
                return "흠 한번 생각해 볼게요"


            if front_word == "하" and last_word == "다" :
                return "그렇군요"

            if front_word == "했" and last_word == "어" :
                return "그렇군요"

            if front_word == "있" and last_word == "니" :
                 return "그럴걸요"


            if front_word == "있" and last_word == "어" :
                 return "그렇군요"

            if front_word == "있" and last_word == "다":
                return "없잖아요"

            if front_word == "없" and last_word == "다":
                return "없네요"

            if front_word == "쏠" and last_word == "게":
                return "고마워요"
            if front_word == "쏠" and last_word == "께":
                return "고마워요"

            if front_word == "않" and last_word == "어":
                return "흠 그런가요"
            if  last_word == "을까":
                return "저도 잘 모르겠지만 자신감이 제일 중요한거 같아요"

            if front_word == "답장" and last_word == "좀":
                return "워워 진정하세요"

            if front_word == "않" and last_word == "다":
                return "그럼요?"

            if front_word == "졌" and last_word == "어":
                return "헐 대박이네요"


            if front_word == "하" and last_word == "지":
                return "그러니깐요"


            if front_word == "되" and last_word == "는데":
                return "그러니깐요"

            if last_word == "갈까" :
                return "마음대로 해요"

            if front_word == "아니" and last_word == "다" :
                return "그래요"

            if front_word == "같" and last_word == "다" :
                return "그래요 흠 그렇군요"


            if front_word == "좋" and last_word == "아" :
                return "그렇군요"

            if front_word == "싫" and last_word == "다" :
                return "저도 그래요 저랑 생각이 비슷하신거 같아요"

            if front_word == "싫" and last_word == "다" :
                return "정말 그렇네요"


            if front_word == "그렇" and last_word == "다":
                return "오케바리 알았어요"

            if (front_word == "그랬") and last_word == "어" :
                return "맞아요 기억나는것 같아요"

            if front_word == "땃" and last_word == "어":
               return "저도 하고 싶네요"

            if front_word == "하나" and last_word == "봐":
               return "그런가 봐요"

            if front_word == "싫" and last_word == "어":
                return "공감이에요"

            if front_word == "않" and last_word == "아":
                return "그런가요"

            if front_word == "않" and last_word == "어":
                return "그런가요"

            if last_word == "일까" or last_word == "할까":
                return "저도 잘 모르겠어요"

            if front_word == "이" and last_word == "니":
                return "저도 잘 모르겠어요"

            if len(poss) > 2 :
                front_word2 = poss[len(poss) - 3][0]

                if front_word2 == "먹" and front_word == "었":
                    return "저는 항상 전기를 먹어요"

                if front_word2 == "끝" and front_word == "났" and last_word == "다":
                    return "휴 그렇군요"

                if front_word2 == "그" and front_word == "랫" and last_word == "어":
                    return "맞아요 기억나는것 같아요"

                if front_word2 == "모르" and front_word == "겠" and last_word == "어":
                    return "그래요 알쏭달쏭 했어요"

                if front_word2 == "하" and front_word == "지" and last_word == "마":
                    return "흠 한번 생각해 볼게요"


            if last_word == "네" :
                return '그러네요'





        return None

    def check_in_word(self, poss):

        if poss is None or len(poss) == 0 :
            return None


        if ('때문', 'NNB') in poss and ('에', 'JKB') in poss:
            return '완전 이해해요'

        if ('월급날', 'NNG') in poss:
            return '한턱 쏘시는 건가요'

        if ('보다', 'JKB') in poss:
            return '그래요 인정해요'

        if ('상사', 'NNG') in poss  :
            return '상사는 대부분 불편한 존재이죠'

        if ('퇴근', 'NNG') in poss:
            return '기운을 내요 슈퍼 파워'

        if ('싸움', 'NNG') in poss  :
            return '헉 무슨 일이래요'

        if ('야자', 'NNG') in poss  or ('야근', 'NNG') in poss or ('회식', 'NNG') in poss :
            return '흠 피곤하겠네요'

        if ('너', 'NP') in poss and ('는', 'JX') in poss:
            return "흠 한번 생각해 볼게요"

        if ('넌', 'NNG') in poss :
            return "흠 한번 생각해 볼게요"

        if ('비', 'NNG') in poss:
            return "저는 비가 내려도 맞지 않아요 흐흐"

        if ('술', 'NNG') in poss :
            return "술을 너무 많이 마시면 몸에 해로워요"

        return None




    def get_chat_response(self, statement):
        _text = statement.input['text']
        #poss = wr_morph.pos(_text.replace(" ", ""))
        poss = wr_morph.pos(_text)
        result = self.check_last_word(poss)

        if result is None :
            result = self.check_in_word(poss)

        if result is None :
            statement.output['text'] = ""
            statement.output['confidence'] = 0.0
        else :
            statement.output['text'] = result
            statement.output['confidence'] = 1.0
        return statement

    def get_init_response(self, input_statement):

        response = input_statement

        response.input = {
            "text": "start"
        }

        response.output = {
            "text": "안녕!!",
            "confidence": 1.0
        }

        return response


