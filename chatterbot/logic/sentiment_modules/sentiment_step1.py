import numpy as np
import pickle
import random



class SentimentStep1():
    """
    A logic adapter that returns a response based on known responses to
    the closest matches to the input statement.
    """

    def __init__(self, mecab, model_dir):

        self.sentiment_morph = mecab
        self.SENTIMENT_DATA_PAHT = model_dir + '/sentiment_data'

    def sentiment_filter_words(self, sent):
        poss = self.sentiment_morph.pos(sent)
        temps = []
        for word, pos in poss:
            if (word == '하' and pos == 'XSA') or (word == '하' and pos == 'XSV'): continue
            if (word == '야' and pos == 'JX') or (word == '야' and pos == 'EC') or (
                    word == '야' and pos == 'VCP+EF'): continue
            if (word == '네' and pos == 'EC') or (word == '네' and pos == 'XSN') or (
                    word == '네' and pos == 'XSA+EC'): continue
            if word == '다': continue
            if word == '하': continue
            if word == '아' and (pos == 'EC' or pos == 'JKV'): continue
            if word == '이' and (pos == 'JKS' or pos == 'VCP'): continue
            if word == '어' and pos == 'EC': continue
            if word == '이야' and pos == 'JX': continue
            if word == '았' and pos == 'EP': continue
            if word == '게' and pos == 'EC': continue
            if word == '습니다' and pos == 'EF': continue
            if word == '는구나' and pos == 'EC': continue
            if word == '는' and pos == 'ETM': continue
            if word == '거' and pos == 'NNB': continue
            # if word == '었' and pos == 'EP'  : continue
            if word == '을' and pos == 'ETM': continue
            if word == '음' and pos == 'ETN': continue
            if word == '어요' and pos == 'EF': continue
            if word == '는' and pos == 'JX': continue
            if word == '지' and pos == 'EC': continue
            if word == '고' and pos == 'EC': continue

            if word == '은데' and pos == 'EC': continue
            if word == '는데' and pos == 'EC': continue

            if word == '나' and pos == 'EC': continue
            if word == '가' and pos == 'JKS': continue

            if word == '해요' and pos == 'XSV+EC': continue

            temps.append(word)
        return temps


    def check_lonely(self, poss):
        #respone_text = ["제가 옆에 있잖아요 항상 옆에서 힘이 되어 줄게요",
        #                "제가 항상 옆에 있을게요 우리 즐거운 이야기 해요",
        #                "제가 항상 옆에 있을게요 우리 맛있는거 먹고 기운 내요"]



        if ('전화', 'NNG') in poss and ('안', 'MAG') in poss :
            return True

        if ('아무', 'NP') in poss and ('도', 'JX') in poss and ('없', 'VA') in poss :
            return True


        if ('혼자', 'MAG') in poss and ('있', 'VV') in poss and ('는', 'ETM') in poss \
                and ('느낌', 'NNG') in poss :
            return True

        if ('연락', 'NNG') in poss and ('할', 'XSV+ETM') in poss and ('사람', 'NNG') in poss \
                and ('없', 'VA') in poss  :
            return True


        if ('연락', 'NNG') in poss and ('한', 'XSV+ETM') in poss and ('사람', 'NNG') in poss \
                and ('없', 'VA') in poss  :
            return True

        if ('살', 'VV') in poss and ('기', 'ETN') in poss and ('막막', 'XR') in poss \
                and ('하', 'XSA') in poss:
            return True

        if ('아무', 'NP') in poss and ('도', 'JX') in poss and ('없', 'VA') in poss :
            return True

        if ('자살', 'NNG') in poss and ('하', 'XSV') in poss and ('싶', 'VX') in poss :
            return True

        if ('사', 'VV') in poss and ('는', 'ETM') in poss and ('지긋', 'VR') in poss :
           return True

        if ('사', 'VV') in poss and ('는', 'ETM') in poss and ('지긋지긋', 'MAG') in poss:
            return True

        if ('혼자', 'NNG') in poss and ('느낌', 'NNG') in poss:
            return True

        if ('혼자', 'NNG') in poss and ('밖에', 'JX') in poss and ('없', 'VA') in poss :
            return True

        if ('친구', 'NNG') in poss and ('없', 'VA') in poss :
            return True

        if ('쓸쓸', 'XR') in poss :
            return True

        return False


    def predict(self, query):
        predicted = self.wd_predict(query)

        if predicted is not None :

            return "평가", predicted

        predicted = self.sd_predict(query)

        if predicted is None:
            return None, None

        return "내감정", predicted

    def sd_check(self, tokens):
        if len(tokens)  == 0 : return False

        if len(tokens) == 1 and '신' in tokens: return True
        if len(tokens) == 1 and '좋' in tokens: return True
        if len(tokens) == 1 and '헤어졌' in tokens: return True

        if len(tokens) == 1 : return False


        # if len(tokens) == 1 and ('남자' in tokens or '여자' in tokens or 'w' in tokens) : return False

        #if len(tokens) < 2 : return False

        if '안' in tokens :
            return False

        if tokens[0] == '뭐' :
            return False

        if '하나' in tokens and '봐' in tokens : return False

        if '뭐' in tokens and '있' in tokens: return False

        if '용돈' in tokens and '줬' in tokens: return False

        if '뭐' in tokens and '해' in tokens: return False

        if '응' in tokens and '그래' in tokens: return False

        if '싶' in tokens and '자살' not in tokens: return False

        if '시험' in tokens and '성적' not in tokens: return False

        if '성적' in tokens and '나왔' not in tokens: return False

        if '먹' in tokens and '었' in tokens and '맛있' not in tokens: return False

        if ('남자' in tokens or '여자' in tokens) and '헤어졌' in tokens: return True

        if ('남자' in tokens or '여자' in tokens) and '생겼' not in tokens: return False

        return True

    def sd_predict(self, query):

        """

        :param query:
        :return:
        """

        is_sad = self.check_sad_dic(query)

        if is_sad : return 2

        is_happy = self.check_happy_dic(query)

        if is_happy: return 1

        tokens = self.sentiment_filter_words(query)

        if len(tokens) == 0 :
            return None

        if "어때" in query :
            return None

        if tokens[len(tokens) - 1] == '먹' :
            return None

        if query[len(query) - 1] == '니' or  query[len(query) - 1] == '?':
            return None
        print("xxxxx ==> ",  query[len(query) - 1], query[len(query) - 2] )
        if len(query)  > 1 and   query[len(query) - 1] == '어' and  query[len(query) - 2] == '있':
            return None

        is_sd = self.sd_check(tokens)

        if not is_sd : return None

        if len(tokens) > 1 and  '안' in tokens and '좋' in tokens :
            return 2


        if len(tokens) > 1 and  '우울해' in tokens and '안' not in tokens :
            return 2

        if len(tokens) > 2 and '기분' in tokens and '짱' in tokens and '않' not in tokens and '안' not in tokens:
            return 1

        if len(tokens) > 2 and '기분' in tokens and '않' in tokens and '좋' in tokens:
            return 2

        if len(tokens) > 3 and '가' in tokens and '좋' in tokens and '지' in tokens and '너' not in tokens:
            return None


        if len(tokens) > 2 and '좋' in tokens and '지' in tokens and '않' in tokens and '기분' in tokens:
            return 2

        if len(tokens) > 2 and '좋' in tokens and '지' in tokens and '않' in tokens and '마음' in tokens:
            return 2

        if len(tokens) > 2 and '좋' in tokens and '지' in tokens and '않' in tokens:
            return None

        if len(tokens) > 1 and '기분' in tokens  and '좋' in tokens:
            return 1

        new_vec = self.sd_count_vect.transform([" ".join(tokens)]).toarray()
        mask_total_vec = np.ones_like(self.sd_total_vector)
        mask_total_vec[self.sd_total_vector <= 0] = 0
        mask_vec = np.ones_like(new_vec[0])
        mask_vec[new_vec[0] <= 0] = 0

        index = np.argmax(mask_total_vec.dot(mask_vec.T))

        mask = mask_total_vec[index] & mask_vec
        mask_cnt = np.sum(mask)

        #print("dadasd mask cnt : ", mask_cnt)
        if mask_cnt == 0: return None

        index = np.argmax(mask)

        print(self.sd_count_vect.get_feature_names()[index])
        #if mask_cnt == 1 and len(self.sd_count_vect.get_feature_names()[index]) < 2: return None

        if mask_cnt == 1 :
            word = self.sd_count_vect.get_feature_names()[index]
            if word not in ['좋', '신', '헤어졌', '신나'] :
                return None


        prob = mask_cnt / len(tokens)
        #print(np.sum(mask), prob)

        # if prob < 0.5 : return None
        predicted = self.sd_clf.predict(new_vec)
        # prob = clf2.predict_proba(new_vec)
        print(predicted)
        return predicted[0]


    def wd_check(self, tokens):

        if len(tokens)  == 0 : return False

        if '공부' in tokens : return False

        if '먹' in tokens: return False

        if len(tokens)  == 1 and ('잘' in tokens or '최고' in tokens or '괜찮' in tokens or '굿' in tokens
        or '재미있' in tokens or '지리' in tokens or '짱' in tokens or '멍청이' in tokens or '멍청' in tokens or '별로' in tokens) : return True

        if len(tokens) < 2 : return False

        if '별로' in tokens and '기분' in tokens: return False

        if '별로' in tokens and '맛' in tokens: return False


        if '생겼' in tokens and '못' not in tokens: return False

        if '똥' in tokens and '빵꾸' not in tokens: return False



        if len(tokens) > 2 and '너' not in tokens and  '좋' in tokens and '지' in tokens:
            return False

        return True



    def wd_predict(self, query):

        """

        :param query:
        :return:
        """


        is_dont_good = self.check_dont_good_dic(query)

        if is_dont_good :
            return 2

        tokens = self.sentiment_filter_words(query)

        if len(tokens) == 0:
            return None

        is_check = self.wd_check(tokens)

        print("===> is_check : ", is_check)

        if not is_check : return None



        if '별로' in tokens and '너' in tokens: return 2

        if '기분' in tokens : return None

        if '먹' in tokens: return None


        if len(tokens) == 2 and  tokens[0] == '별론' and (tokens[1] == '대' or tokens[1] == '데'):
            return 2
        if len(tokens) == 1 and tokens[0] == '별론데' :
            return 2

        if len(tokens) > 3 and '너' in tokens and '가' in tokens and '좋' in tokens and '지' in tokens:
            return 2


        new_vec = self.wd_count_vect.transform([" ".join(tokens)]).toarray()
        mask_total_vec = np.ones_like(self.wd_total_vector)
        mask_total_vec[self.wd_total_vector <= 0] = 0
        mask_vec = np.ones_like(new_vec[0])
        mask_vec[new_vec[0] <= 0] = 0

        index = np.argmax(mask_total_vec.dot(mask_vec.T))

        mask = mask_total_vec[index] & mask_vec
        mask_cnt = np.sum(mask)
        index = np.argmax(mask)

        prob = mask_cnt / len(tokens)


        if mask_cnt == 1 :
            word = self.wd_count_vect.get_feature_names()[index]
            if word not in ['잘', '최고', '괜찮', '굿', '재미있', '지리', '짱', '멍청이', '멍청', '별로'] :
                return None

        if prob < 0.5: return None
        predicted = self.wd_clf.predict(new_vec)
        return predicted[0]


    def check_full(self, text):

        _text = text.replace(" ", "")
        keywords = ['배불', '배부르', '배터질', '배불르', '배터지', '배불러', '트름', '꺼억', '소화제']

        for keyword in keywords:
            if keyword in _text:
                return True
        return None


    def check_fear(self, text):

        _text = text.replace(" ", "")
        keywords = ['섬츳', '흉측', '섬틋', '무서', '무섭', '섬뜩']

        for keyword in keywords:
            if keyword in _text:
                return True
        return None

    def check_afraid(self, text):
        _text = text.replace(" ", "")
        keywords = ['드려워', '두렵', '두려워']

        if '안' in _text or '않' in _text :
            return None

        for keyword in keywords:
            if keyword in _text:
                return True
        return None

    def check_warry(self, text):

        _text = text.replace(" ", "")
        keywords = ['고민', '걱정', '불안', '꺼름칙', '불확실']

        for keyword in keywords:
            if keyword in _text:
                return True
        return None


    def check_hurry(self, text):

        _text = text.replace(" ", "")
        keywords = ['빨리', '얼른', '급해']

        for keyword in keywords:
            if keyword in _text:
                return True
        return None


    def check_sorrow(self, text):

        _text = text.replace(" ", "")
        keywords = ['죽었']

        for keyword in keywords:
            if keyword in _text:
                return True
        return None



    def check_likeable(self, poss):

        if ('안', 'MAG') in poss  or ('않', 'VX') in poss or ('뭐', 'NP') in poss or ('을까', 'EC') in poss or ('을까', 'EF') in poss  or ('니', 'EC') in poss:
            return None


        if ('좋', 'VA') in poss or ('좋아해', 'VV+EC') in poss or ('좋아해', 'VV+EF') in poss or ('좋아하', 'VV') in poss :
            return True

        return None

    def check_unlikeable(self, text):

        _text = text.replace(" ", "")

        if '먹' in _text :
            return None


        keywords = ['미워', '극혐', '나빠', '징그러', '징그럽', '밉', '나쁘', '나빴', '별로', '불호', '씹불호', '바퀴벌레', '토악질', '토', '역겹', '구역질', '싫', '시러', '시르']

        for keyword in keywords:
            if keyword in _text:
                return True
        return None


    def check_angry(self, text):

        _text = text.replace(" ", "")
        keywords = ['화난', '싸울', '화나', '때릴', '때려', '화났', '뒤진', '뒤질', '장난하', '열받', '미친', '쒸익쒸익', "화가나", "화가난"]

        for keyword in keywords:
            if keyword in _text:
                return True
        return None

    def check_sorry(self, text):

        _text = text.replace(" ", "")
        keywords = ['미안', '잘못', '죄송', '사죄', '유감', '반성', '실수']

        for keyword in keywords:
            if keyword in _text:
                return True
        return None



    def check_stuffy(self, text):

        _text = text.replace(" ", "")

        if _text == "휴" :
            return True

        keywords = ['답답', '미세먼지', '깝깝', '갑갑', '교통정체', '교통체증', '막히', '막혔', '막혀']
        if '사람' in _text and '많' in _text :
            return True

        for keyword in keywords:
            if keyword in _text:
                return True
        return None


    def check_fright(self, text):

        _text = text.replace(" ", "")
        keywords = ['놀랐', '깜짝', '놀랬', '헐', '헐랭', '와우', '깜짝', '놀래', '버그', '오류', '에러', '불났']

        for keyword in keywords:
            if keyword in _text:
                return True
        return None


    def check_sad_dic(self, text):

        _text = text.replace(" ", "")
        keywords = ['속상', '슬퍼', '헤어졌', '이별', '외로워', '괴로움', '외로움', '괴로워', '눈물', '슬프', '꼴찌', '혼났', '망했',
                    '망함', '위로', '우울', '외롭' , '슬픈', '울고싶', '헤어짐', '가슴아파', '서운', '섭섭', '싸웠', '다퉜', '꼴등', '짤렸',
                    '명퇴', '마음아파', '울적', '애잔', '야단쳤', '가버렸', '서러워', '서럽', '다퉈', '미워','밉', '꾸중', '외로운', '싸웠', '혼냈', '슬픈',
                    '야단', '뺏겼', '뺏어갔', '싸웠', '야근', '슬펐', '가슴아프', '마음아프', '바람폈', '바람핀', '망했', '괴롭', '혼냈'
                    ]
        for keyword in keywords:
            if keyword in _text:
                return True
        return None


    def check_happy_dic(self, text):

        _text = text.replace(" ", "")

        if "없" in _text or "안" in _text or "어" in _text :
            return None

        keywords = ['신나', '기뻐', '재미' , '재밌', '재밋', '즐거', '신난', '즐겁', '놀았',
                    '행복', '용돈', '기쁘', '기쁨', '최고', '행복사', '해피', '기뻤', '개꿀']
        for keyword in keywords:
            if keyword in _text:
                return True
        return None




    def check_dont_good_dic(self, text):

        _text = text.replace(" ", "")
        keywords = ['시끄', '멍청', '이상', '쓰레기', '딴소리', '이상하', '개판', '인식', '한심',
                    '모르', '반말', '헛소리', '개소리', '씹소리', '이따구', '돈아깝', '불편', '딴말', '맞을래', '맞고싶', '부족', '안좋']
        for keyword in keywords:
            if keyword in _text:
                return True
        return None



    def check_wish(self, text):
        _text = text.replace(" ", "")

        if "뭐" in _text :
            return None

        keywords = ['가고싶', '보고싶', '놀고싶', '먹고싶', '하고싶', '가지고싶', '갖고싶', '듣고싶', '치고싶', '자고싶', '마시고싶', '싶다', '싶어']

        for keyword in keywords:
            if keyword in _text:
                return True
        return None


    def check_irritation(self, text):
        _text = text.replace(" ", "")
        keywords = ['짜증', '쓰레기', '나빠', '그만', '신경꺼', '장난하', '짱나', '짱난', '장난치',
                    '오바', '뭐래', '미쳤', '화돋구', '화나', '어이없', '돌겠', '저리가', '죽겠', '미쳤',
                    '불편' ,'뭐라', '트롤', '빡치', '빡쳤', '노답', '좆노답']
        for keyword in keywords:
            if keyword in _text:
                return True
        return None

    def check_boring(self, text):
        _text = text.replace(" ", "")

        if "재미" in _text and "없" in _text :
            return True

        keywords = ['심심', '노잼', '따분', '지루', '루즈', '뻔하', '하품', '지겨', '지겹', '씹노잼']
        for keyword in keywords:
            if keyword in _text:
                return True
        return None

    def check_disappointment(self, text):

        _text = text.replace(" ", "")

        if '퇴근' in _text and '못' in _text:
            return True

        if '시험' in _text and '망' in _text:
            return True

        if '면접' in _text and '망' in _text:
            return True

        keywords = ['졌어', '졌네', '폭락', '폭낙', '혼났', '개털', '떡낙', '떡락', '떨어졌', '지각', '누락']
        for keyword in keywords:
            if keyword in _text:
                return True
        return None

    def get_chat_response(self, statement):

        _text = statement.input['text']

        query = _text.replace(" ", "")
        poss = self.sentiment_morph.pos(query)
        is_lonely = self.check_lonely(poss)

        if is_lonely :
            return "내감정", "외로움"

        if self.check_warry(_text) is not None :
            return "내감정", "불안"


        if self.check_fear(_text) is not None :
            return "내감정", "무서움"

        if self.check_afraid(_text) is not None :
            return "내감정", "두려움"


        if self.check_full(_text) is not None :
            return "내감정", "배부름"

        if self.check_unlikeable(_text) is not None :
            return "내감정", "비호감"

        if self.check_angry(_text) is not None :
            return "내감정", "분노"


        if self.check_hurry(_text) is not None :
            return "내감정", "다급함"

        if self.check_wish(_text) is not None :
            return "내감정", "바램"

        if self.check_irritation(_text) is not None :
            return "내감정", "짜증"

        if self.check_sorry(_text) is not None :
            return "내감정", "미안함"


        if self.check_stuffy(_text) is not None :
            return "내감정", "답답함"

        if self.check_fright(_text) is not None :
            return "내감정", "놀람"


        if self.check_likeable(poss) is not None :
            return "내감정", "호감"


        if self.check_disappointment(_text) is not None :
            return "내감정", "실망"


        if self.check_boring(_text) is not None :
            return "내감정", "지루함"

        if self.check_sorrow(_text) is not None :
            return "내감정", "슬픔"


        meta_data = pickle.load(open(self.SENTIMENT_DATA_PAHT + "/sentiment.meta", 'rb'))
        self.sd_count_vect = meta_data["sd_cont"]
        self.wd_count_vect = meta_data["wd_cont"]
        self.wd_total_vector = meta_data["wd_total_vec"]
        self.sd_total_vector = meta_data["sd_total_vec"]
        self.sd_clf = meta_data["sd_clf"]
        self.wd_clf = meta_data["wd_clf"]

        reaction, sentiment = self.predict(_text)

        if reaction == "평가" :
            wd_names =  {1: "평가긍정", 2:"평가부정"}
            return "제품평가", wd_names[sentiment]


        if reaction == "내감정" :
            sd_names = {1: "기쁨", 2: "우울함"}
            return "내감정", sd_names[sentiment]

        #
        # if reaction is None :
        #     statement.output['text'] = ''
        #     statement.output['confidence'] = 0.0
        # else :
        #     statement.output['text']  = self.response_sents(reaction, sentiment)
        #     statement.output['confidence'] = 1.0
        return None, None


