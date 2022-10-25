from chatterbot.logic import CustomAdapter
from konlpy.tag import Mecab

class DicPatternAdapter(CustomAdapter):
    def can_process(self, statement):
        """
        Check that the chatbot's storage adapter is available to the logic
        adapter and there is at least one statement in the database.
        """
        return True
        # return self.chatbot.storage.has_chatbot(statement.chatbot_id)

    def process(self, statement):

        return self.get_chat_response(statement)


    def get_chat_response(self, statement):

        dbdic_morph = Mecab()

        _text = statement.input['text']

        poss = dbdic_morph.pos(_text)

        # print("----->", poss)

        response = self.play_check_me(poss)

        if response is None :
            response = self.what_check_song(poss)

        if response is None :
            response = self.what_check_eat(poss)

        if response is None :
            response = self.what_check_likes(poss)

        if response is None :
            response = self.what_check_search(poss)

        if response is None:
            response = self.what_check_parents(poss)

        if response is None:
            response = self.what_check_feels(poss)

        if response is None :
            response = self.what_check_study(poss)


        if response is None :
            response = self.what_check_etc(poss)


        if response is None :
            response = self.sick_check(poss, _text)


        if response is None :
            response = self.toilet_check(poss, _text)

        if response is None:
            response = self.check_shyness(poss, _text)

        if response is None :
            response = self.molestia_check(poss, _text)


        if response is None :
            response = self.cool_check(poss, _text)


        if response is None :
            response = self.hot_check(poss, _text)


        if response is None :
            response = self.tired_check(poss, _text)

        if response is None :
            response = self.hard_check(poss, _text)


        if response is None :
            response = self.dirty_check(poss, _text)

        if response is None :
            response = self.check_how_are_you(poss, _text)

        if response is None:
            response = self.check_dont_tasty(poss, _text)

        if response is None:
            response = self.good_job_check(poss, _text)


        if response is None:
            response = self.born_check(poss, _text)


        if response is None:
            response = self.check_tasty(poss, _text)

        if response is None:
            response = self.cool_check(poss, _text)

        if response is None:
            response = self.consider_check(poss, _text)

        if response is None:
            response = self.cleaning_check(poss, _text)

        if response is None:
            response = self.clean_check(poss, _text)

        if response is None:
            response = self.negative_response_check(poss, _text)

        if response is None:
            response = self.check_death(_text)


        intents = self.get_intents()
        
        if response is None or response not in intents :
            statement.set_output(
                _text='',
                _module='',
                _intent="학습패턴대화",
                _confidence=0.0
            )
            return statement



        response_text = self.select_response(response_list=intents[response]["output"].split(","))

        statement.set_output(
            _text=response_text,
            _module='',
            _intent=response,
            _confidence=1.0
        )

        return statement



    def born_check(self, poss, text):
        _text = text.replace(" ", "")
        keywords = ['태어났', '태어난', '출생', '제작', '출신', '고향']
        for keyword in keywords:
            if keyword in _text:
                return "어디출신"
        return None


    def sick_check(self, poss, text):

        _text = text.replace(" ", "")
        if ('감기', 'NNG') in poss and ('걸린', 'VV+ETM') in poss:
            return "질병"

        if ('감기', 'NNG') in poss and ('걸렸', 'VV+EP') in poss:
            return "질병"

        if ('감기', 'NNG') in poss and '같아' in _text :
            return "질병"

        if ('몸살', 'NNG') in poss and ('걸린', 'VV+ETM') in poss:
            return "질병"

        if ('몸살', 'NNG') in poss and ('걸렸', 'VV+EP') in poss:
            return "질병"

        if ('몸살', 'NNG') in poss and '같아' in _text:
            return "질병"

        if (('열', 'NNG') in poss or ('열', 'NR') in poss or ('열', 'VV') in poss) and '나' in _text:
            return "질병"

        if ('기침', 'NNG') in poss and '나' in _text:
            return "질병"

        keywords = ['다쳤', '아파', '아픈', '넘어졌', '다친', '아프', '까졌', '아파', '다쳐', '삐었', '쑤셔', '지끈',
                    '쑤신', '쑤시', '통증', '찌뿌둥', '결린', '결렸', '시리', '시린', '따가', '따갑', '아프']

        for keyword in keywords:
            if keyword in _text:
                return "질병"
        return None

        return None


    def check_death(self, text):
        _text = text.replace(" ", "")

        keywords = ['죽음', '죽는', '죽을']

        for keyword in keywords:
            if keyword in _text:
                return "죽음"
        return None



    def dirty_check(self, poss, text):

        _text = text.replace(" ", "")
        keywords = ['너저분', '냄새', '지저분', '방구', '더러', '찝찝', '방귀']

        for keyword in keywords:
            if keyword in _text:
                return "지저분"
        return None



    def cool_check(self, poss, text):

        _text = text.replace(" ", "")
        keywords = ['시원', '아이스크림', '수박', '에어컨', '선풍기', '얼음', '빙수', '아이스']

        for keyword in keywords:
            if keyword in _text:
                return "시원함"
        return None



    def negative_response_check(self, poss, text):

        _text = text.replace(" ", "")
        keywords = ['극혐', '아니', '아냐', '아닌', '아니거든', '노노']

        for keyword in keywords:
            if keyword in _text:
                return "부정응답"
        return None




    def consider_check(self, poss, text):

        _text = text.replace(" ", "")
        keywords = ['조심', '양보', '지켜줄', '도와줄']

        for keyword in keywords:
            if keyword in _text:
                return "배려"
        return None


    def cleaning_check(self, poss, text):

        _text = text.replace(" ", "")
        keywords = ['정리', '닦자', '치워', '치우', '청소', '닦으', '청소기', '행주',
                    '쓸자', '쓸어', '닦어', '닦아', '방청소', '걸레질', '물청소', '먼지', '환기', '치울']

        for keyword in keywords:
            if keyword in _text:
                return "청소"
        return None


    def clean_check(self, poss, text):

        _text = text.replace(" ", "")
        keywords = ['씻었', '샤워', '세수', '온천', '비누', '샴푸']

        for keyword in keywords:
            if keyword in _text:
                return "깔끔"
        return None




    def check_how_are_you(self, poss, text):

        if ('하', 'VV') in poss and ('어떤', 'MM') in poss :
            return "뭐해"

        if ('하고', 'JKB') in poss and ('무엇', 'NP') in poss :
            return "뭐해"

        if ('무엇', 'NP') in poss and ('해', 'VV+EF') in poss :
            return "뭐해"

        if ('무엇', 'NP') in poss and ('해', 'VV+EC') in poss:
            return "뭐해"

        _text = text.replace(" ", "")
        keywords = ['뭐해', '뭐하고', '뭐했', '뭐했었', '뭐하면서', '지냈니', '지냈어', '근황', '뭐함', '뭐하는', '뭐하길래', '뭐혀', '뭐하니']

        for keyword in keywords:
            if keyword in _text:
                return "뭐해"
        return None


    def check_dont_tasty(self, poss, text):
        _text = text.replace(" ", "")
        keywords = ['노맛', '맛없', '맛이없', '좆노맛']

        for keyword in keywords:
            if keyword in _text:
                return "맛없다"
        return None




    def check_tasty(self, poss, text):
        _text = text.replace(" ", "")
        keywords = ['맛있', '맛잇', '맛이있', '맛이잇', '꿀맛', '존맛', '존맛탱']

        if len(_text) == 0 :
            return None

        if _text[len(_text) - 1] == '지' or _text[len(_text) - 1] == '줘' or _text[len(_text) - 1] == '?':
            return None


        for keyword in keywords:
            if keyword in _text:
                return "맛있다"
        return None



    def cool_check(self, poss, text):
        _text = text.replace(" ", "")
        keywords = ['추워', '추운', '춥', '얼어']

        for keyword in keywords :
            if keyword in _text:
                return "추워"
        return None


    def hard_check(self, poss, text):
        _text = text.replace(" ", "")
        keywords = [ '힘들', '어려워', '어렵', '어려운', '힘든', '힘이없', '어려울', '힘드시', '힘없', '힘겹', '힘겨',  '쉴래', '쉴까', '쉬자', '쉬어']

        for keyword in keywords :
            if keyword in _text:
                return "힘듬"
        return None


    def good_job_check(self, poss, text):

        _text = text.replace(" ", "")

        if "합격" in _text or "통과" in _text or "패스" in _text or "pass" in _text :

            if  "됬" in _text  and "안" not in _text:
                return "축하"

            if  "됐" in _text  and "안" not in _text:
                return "축하"

            if  "했" in _text and "안" not in _text:
                return "축하"

            if  "햇" in _text and "안" not in _text:
                return "축하"

        keywords = ['축하', '생일', '월급', '선물', '기프티콘']

        for keyword in keywords:
            if keyword in _text:
                return "축하"
        return None

    def tired_check(self, poss, text):
        _text = text.replace(" ", "")

        if "않" in _text or  "안" in _text :
            return None
        
        keywords = ['졸려', '피곤', '졸리', '피로', '쉬어', '잘래', '지쳤', '잠', '이불', '배게', '침대', '수면', '숙면', '졸립', '자자', '졸린', '자고', '쉴래', '불면증', '잘자']
        for keyword in keywords :
            if keyword in _text:
                return "피곤함"
        return None

    def hot_check(self, poss, text):
        _text = text.replace(" ", "")
        keywords = ['땀', '더위', '후덥지', '후', '덥', '열사병']

        for keyword in keywords :
            if keyword in _text:
                return "더위"
        return None

    def molestia_check(self, poss, text):
        _text = text.replace(" ", "")
        keywords = ['귀찮', '나중', '성가시', '성가셔', '이따가', '귀차니즘', '게을러', '게으름', '무기력', '번아웃']

        for keyword in keywords :
            if keyword in _text:
                return "귀찮음"
        return None

    def toilet_check(self, poss, text):
        _text = text.replace(" ", "")

        if ('화장실', 'NNG') in poss and '갈' in _text:
            return "화장실"

        if ('화장실', 'NNG') in poss and '가고' in _text:
            return "화장실"

        if ('화장실', 'NNG') in poss and '가고' in _text:
            return "화장실"

        if (('오줌', 'NNG') in poss or ('똥', 'NNG') in poss or ('응가', 'NNG') in poss or ('쉬', 'MAG') in poss) and '마려' in _text:
            return "화장실"

        if (('오줌', 'NNG') in poss or ('똥', 'NNG') in poss or ('응가', 'NNG') in poss or ('쉬', 'MAG') in poss) and '나' in _text:
            return "화장실"


        return None

    def check_shyness(self, poss, text):
        _text = text.replace(" ", "")

        if '부끄러' in _text :
            return '부끄러움'

        if '창피' in _text :
            return '부끄러움'

        if '챙피' in _text :
            return '부끄러움'

        if '쪽팔' in _text:
            return '부끄러움'

    def what_check_etc(self, poss):
        if ('키', 'NNG') in poss and ('몇', 'MM') in poss:
            return "키가몇이야"

        if ('키', 'NNG') in poss and ('어느', 'MM') in poss and ('정도', 'NNG') in poss:
            return "키가몇이야"

        if ('놀리', 'VV') in poss and ('냐', 'EC') in poss:
            return "놀리냐"

        if ('놀리', 'VV') in poss and ('냐', 'EF') in poss:
            return "놀리냐"



        #if ('할', 'VV+ETM') in poss and ('수', 'NNB') in poss and ('있', 'VV') in poss and ('을까', 'EC') in poss:
        #    return "노력하면 충분히 할수 있을꺼예요 화이팅"


        if ('무슨', 'MM') in poss and ('생각', 'NNG') in poss:
            return "무슨생각"

        if ('무슨', 'MM') in poss and ('생각', 'NNG') in poss:
            return "무슨생각"

        if ('어떤', 'MM') in poss and ('생각', 'NNG') in poss:
            return "무슨생각"

        if ('무엇', 'NP') in poss and ('생각', 'NNG') in poss:
            return "무슨생각"

        #if ('잘', 'MAG') in poss and ('지냈', 'VV+EP') in poss:
        #    return "저는 늘 행복하게 지내고 있어요"

        #if ('괜찮', 'VA') in poss and ('아', 'EC') in poss:
        #    return "그렇군요"

        if (('뭐', 'IC') in poss or ('뭐', 'NP') in poss) and ('생각', 'NNG') in poss:
            return "무슨생각"



        # if ('좋아해', 'VV+EC') in poss and ('안', 'MAG') not in poss and ('않', 'VX') not in poss and (
        # '싫', 'VA') not in poss:
        #     return "우와 그랬구나"
        #
        # if ('사랑', 'NNG') in poss and ('안', 'MAG') not in poss and ('않', 'VX') not in poss and ('싫', 'VA') not in poss:
        #     return "우와 그랬구나"

        # if ('좋', 'VA') in poss and ('기분', 'NNG') in poss and ('아', 'EC') in poss and ('안', 'MAG') not in poss and (
        # '않', 'VX') not in poss:
        #     return "저도 기분이 좋아요"

        return None


    def what_check_search(self, poss):
        if ('검색', 'NNG') in poss and ('해', 'XSV+EC') in poss:
            return "검색해줘"

    def what_check_likes(self, poss):

        is_true = False
        if ('어떤', 'MM') in poss and ('좋', 'VA') in poss and ('아', 'EC') in poss:
            is_true = True

        if ('어떤', 'MM') in poss and ('만들', 'VV') in poss:
            is_true = True

        if ('무엇', 'NP') in poss and ('좋아해', 'VV+EC') in poss:
            is_true = True

        if ('뭐', 'IC') in poss and ('좋', 'VA') in poss and ('아', 'EC') in poss and ('해', 'VV+EC') in poss:
            is_true = True

        if ('뭐', 'NP') in poss and ('좋아해', 'VV+EC') in poss:
            is_true = True

        if ('뭘', 'NP+JKO') in poss and ('좋아해', 'VV+EC') in poss:
            is_true = True

        if is_true:
            if ('그림', 'NNG') in poss:
                return "그림좋아해"

            if ('음악', 'NNG') in poss or ('노래', 'NNG') in poss:
                return "음악좋아해"

            if ('요리', 'NNG') in poss or ('음식', 'NNG') in poss:
                return "요리좋아해"
            return "뭐를좋아해"
        return None


    def what_check_parents(self, poss):


        if ('엄마', 'NNG') in poss and ('어디', 'NP') in poss and ('있', 'VA') in poss:
            return "엄마아빠어디있어"

        if ('아빠', 'NNG') in poss and ('어디', 'NP') in poss and ('있', 'VA') in poss:
            return "엄마아빠어디있어"


        return None

    def what_check_feels(self, poss):
        if ('기분', 'NNG') in poss and ('어때', 'VA+EC') in poss:
            return "기분어때"

        if ('기분', 'NNG') in poss and ('어때', 'VA+EF') in poss:
            return "기분어때"

        if ('기분', 'NNG') in poss and ('니', 'EC') in poss:
            return "기분어때"

        if ('무슨', 'MM') in poss and ('기분', 'NNG') in poss and ('들', 'VV') in poss:
            return "기분어때"
        if ('어떤', 'MM') in poss and ('기분', 'NNG') in poss and ('들', 'VV') in poss:
            return "기분어때"

        return None

    def play_check_me(self, poss):
        if len(poss) == 2 and ('놀', 'VV') in poss and ('자', 'EC') in poss:
            return "놀자"

        if ('나', 'NP') in poss and ('랑', 'JKB') in poss and ('놀', 'VV') in poss and ('자', 'EC') in poss:
            return "놀자"

        if (('놀', 'VV') in poss or ('아', 'EC') in poss) and ('줘', 'VX+EC') in poss:
            return "놀자"

        return None

    def what_check_song(self, poss):

        if ('랩', 'NNG') in poss and ('해', 'XSV+EC') in poss:
            return "랩해줘"

        if ('랩', 'NNG') in poss and ('불러', 'VV+EC') in poss:
            return "랩해줘"

        if ('랩', 'NNG') in poss and ('불러줘', 'VV+EC+VX+EC') in poss:
            return "랩해줘"

        return None


    def what_check_eat(self, poss):
        if ('먹', 'VV') in poss and ('을까', 'EC') in poss:
            return "맛있는거뭐"

        if ('먹', 'VV') in poss and ('을래', 'EC') in poss:
            return "맛있는거뭐"

        if ('뭐', 'IC') in poss and ('먹', 'VV') in poss and ('을까', 'EC') in poss:
            return "맛있는거뭐"

        if ('맛있', 'VA') in poss and ('뭔데', 'NP+VCP+EC') in poss:
            return "맛있는거뭐"

        if ('맛있', 'VA') in poss and ('뭐', 'IC') in poss:
            return "맛있는거뭐"

        if ('맛있', 'VA') in poss and ('어', 'EC') in poss:
            return "맛있는거뭐"

        if ('맛있', 'VA') in poss and ('어', 'EF') in poss:
            return "맛있는거뭐"

        if ('뭐', 'IC') in poss and ('먹', 'VV') in poss:
            return "밥먹었어"

        if ('뭐', 'NP') in poss and ('먹', 'VV') in poss:
            return "밥먹었어"

        if ('어떤', 'MM') in poss and ('먹', 'VV') in poss:
            return "밥먹었어"


        if ('무엇', 'NP') in poss and ('먹', 'VV') in poss:
            return "밥먹었어"

        if ('밥', 'NNG') in poss and ('먹', 'VV') in poss and ('었', 'EP') in poss:
            return "밥먹었어"

        if ('밥', 'NNG') in poss and ('먹', 'VV') in poss and ('수', 'NNB') in poss:
            return "밥먹었어"

        return None


    def what_check_study(self, poss):

        if ('공부', 'NNG') in poss and ('뭐', 'IC') in poss:
            return "공부뭐해"

        if ('무슨', 'MM') in poss and ('공부', 'NNG') in poss:
            return "공부뭐해"

        if ('어떤', 'MM') in poss and ('공부', 'NNG') in poss:
            return "공부뭐해"

        if ('공부', 'NNG') in poss and ('하', 'XSV') in poss:
            return "공부뭐해"

        if ('공부', 'NNG') in poss and ('해', 'XSV+EC') in poss:
            return "공부뭐해"

        return None