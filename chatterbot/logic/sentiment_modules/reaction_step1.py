import json
from sklearn.metrics.pairwise import cosine_similarity
import pickle


class ReactionStep1():
    """
        A logic adapter that returns a response based on known responses to
        the closest matches to the input statement.
        """

    def __init__(self, mecab, DB, model_dir):
        self.sentiment_morph = mecab
        self.output_DB = DB
        self.REACTION_DATA_PAHT = model_dir + '/reaction_data'

    def check_sim_sentence(self, text):

        r_text = text.replace(" ", "")

        if r_text == "뭐해" or r_text == "뭐하냐" or r_text == "뭐햐" or r_text == "뭐하냐고":
            return "근황"
        if r_text in "뭐하고있어" or r_text in '뭐하니' or r_text in '뭐했어':
            return "근황"

        if r_text == "졸립다" or r_text == "졸려" or r_text == "지루해" or r_text == "지루하다" or r_text == "졸리다" or r_text == "잠온다" or r_text == "잠와":
            return "심심해"

        if r_text == "뭐먹을까" or r_text == "뭐먹지" or r_text == "먹을거추천해줘":
            return "배고프다"

        if r_text == "응" or r_text == "어" or r_text == "오케이" or r_text == "그치" or r_text == "그렇구나":
            return "그래"

        if r_text == "와우" or r_text == "깜짝이야" or r_text == "헐":
            return "깜짝"

        if r_text == "너누구니" or r_text == "너누구야" or r_text == "너누구" or r_text == "너뭐야" or r_text == "너누구냐":
            return "누구니"

        if r_text == "좋은거뭐야" or r_text == "좋아하는거뭐야" or r_text == "뭘좋아하니" or r_text == "좋아하는거알려줘" or r_text == "좋아하는게뭐야" or r_text == "좋은게뭐니":
            return "뭐 좋아해"

        if r_text == "싫은거뭐야" or r_text == "싫어하는거뭐야" or r_text == "뭐싫어하니" or r_text == "싫어하는거알려줘" or r_text == "싫어하는게뭐야" or r_text == "싫은게뭐니" or r_text == "싫어하는건뭐야":
            return "뭐 싫어해"

        if r_text == "성별이뭐야" or r_text == "남자니" or r_text == "여자니" or r_text == "너남자니" or r_text == "너여자니" or r_text == "성별알려줘" or r_text == "남자여자" or r_text == "성별뭐야" or r_text == "여자남자":
            return "성별"
        if "개판" in r_text:
            return "개판"
        if "아닌데" in r_text:
            text = r_text.replace("아닌데","아냐")
        if "쌀쌀" in r_text or "쌀 쌀" in r_text:
            text = r_text.replace("쌀쌀", "춥다")
        if "작작" in r_text:
            text = r_text.replace("작작","그만")
        if "개역겹" in r_text:
            text = r_text.replace("개역겹","역겹")
        if "허술" in r_text :
            text = r_text.replace("허술","불편")
        elif "시시" in r_text:
            text = r_text.replace("시시","불편")
        return text

    def get_reaction(self, text):
        def sentiment_filter_words_input(input_text):
            poss = self.sentiment_morph.pos(input_text)
            temps = []
            for word, pos in poss:
                if (word == '하' and pos == 'XSA') or (word == '하' and pos == 'XSV'): continue
                if (word == '야' and pos == 'JX') or (word == '야' and pos == 'EC') or (
                        word == '야' and pos == 'VCP+EF'): continue
                if (word == '네' and pos == 'EC') or (word == '네' and pos == 'XSN') or (
                        word == '네' and pos == 'XSA+EC'): continue
                if word == '다': continue
                if word == '하': continue
                if word == '아' and (pos == 'IC' or pos == 'EC' or pos == 'JKV'): continue
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
                if word == '지' and (pos == 'EC' or pos == 'NNB'): continue
                if '요' in word and pos == 'VA+EC':
                    word = word.replace("요", "")
                if word == '요' and pos == 'JX': continue
                if word == '좀' and pos == 'MAG': continue
                if word == '자' and pos == 'EC': continue
                #if word == '했' and pos == 'XSV+EP': continue
                if word == '면' and pos == 'EC': continue
                if word == '개' and pos == 'NNBC': continue
                if '운' in word and pos == 'VA+ETM':
                    word = word.replace("운","")
                if word == '자' and pos == 'IC' : continue
                #if word == '뭐' and pos == 'IC' : continue
                if word == '냐' and pos == 'EC' : continue
                if word == '너' and pos == 'NP' : continue

                temps.append(word)

            return temps

        def constrainter(senti, text):
            if (senti[0] == '기쁨') and (
                    '안' in text or '좋' in text or '않' in text or '싫' in text):
                return False
            if (senti[0] == '바램') and ('싶' not in text):
                return False
            if (senti[0] == '아픔') and ('먹 었' in text):
                return False
            if (senti[0] == '맛있음' or senti[0] == '맛없음') and ('맛' not in text):
                return False
            if (senti[0] == '깔끔함') and ('었' in text):
                if '씻' not in text:
                    return False
            if senti[0] == '안부':
                print(text)
                if '해' in text:
                    if not '뭐' in text:
                        print(text)
                        print('not 뭐')
                        return False
                if '뭐' in text and '했' in text:
                    if not ('뭐했' in text or '뭐 했' in text):
                        return False
                if '뭐 가' in text:
                    return False
                if '니' in text:
                    if not '뭐' in text:
                        return False
            if (senti[0] == '불만') and ('이' in text):
                if not ('이상' in text or '이 상' in text or '이따구' in text):
                    return False
            if senti[0] == '무서움':
                if '서' in text or '섭' in text:
                    if '무' not in text:
                        return False
                if '섬' in text :
                    if '섬뜩' in text:
                        pass
                    elif '섬츳' in text:
                        pass
                    elif '섬틋' in text:
                        pass
                    else:
                        return False
            if (senti[0] == '지루함') and ('지' in text):
                if '지루' in text:
                    pass
                elif '지겹' in text:
                    pass
                elif '지겨' in text:
                    pass
                else:
                    return False
            elif (senti[0] == '지루함') and ('잼' in text):
                if '노잼' not in text:
                    return False
                elif '잼없' or '잼 없' in text:
                    pass
            if (senti[0] == '비호감') and ('그러' in text):
                if '징' not in text:
                    return False
            if (senti[0] == '정체성성별') and ('남자친구' in text or '여자친구' in text):
                return False
            if (senti[0] == '만족') and ('잘' in text):
                if '하' in text:
                    if '냐' in text:
                        return False
            elif (senti[0] == '만족') and ('했' in text):
                return False
            if (senti[0] == '불만') and ('말' in text):
                if '반말' in text:
                    return True
                elif '딴말' in text:
                    return True
                else :
                    return False
            return True

        # constrainter 제약조건 메소드

        raw_text_len = len(text)

        tagging_text =''
        text = self.check_sim_sentence(text)

        filter_text = sentiment_filter_words_input(text)

        for word_tagging in filter_text:
            tagging_text += word_tagging +' '

        tagging_text = self.check_sim_sentence(tagging_text)

        tagging_text = tagging_text[:-1]

        nng = ['NNG', 'NNP', 'XR', 'MAG']

        tag = self.sentiment_morph.pos(text.replace(" ", ""))
        n = ''
        for i in tag:
            if i[1] in nng:
                n += i[0] +' '
        n = n[:-1]

        print("get reaction ===>", text)

        with open( self.REACTION_DATA_PAHT + '/base_string0611_replace.json', 'r', encoding='utf-8') as f:
            base_replace = json.load(f)
        with open(self.REACTION_DATA_PAHT + '/base_string0618.json', 'r', encoding='utf-8') as f:
            base_tagging = json.load(f)
        # json

        #reaction_sent = pd.read_csv( REACTION_DATA_PAHT+ '/reactiondata - reaction_sent0604_1.csv')
        # 리액션 csv


        loaded_sent_vect_replaced = pickle.load(open(self.REACTION_DATA_PAHT+ '/reaction_vect_sent0611_replace.sav', 'rb'))
        loaded_sent_vect_tagging = pickle.load(open(self.REACTION_DATA_PAHT+ '/reaction_vect_sent0618.sav', 'rb'))

        loaded_model_sent_replaced = pickle.load(open(self.REACTION_DATA_PAHT+ '/reaction_sent0611_replace.sav', 'rb'))
        loaded_model_sent_tagging = pickle.load(open(self.REACTION_DATA_PAHT+ '/reaction_sent0618.sav', 'rb'))
        # 단어벡터, 모델

        sent_replace = loaded_sent_vect_replaced.transform([text.replace(" ", "")])
        sent_tagging = loaded_sent_vect_tagging.transform([tagging_text])
        sent_nng = loaded_sent_vect_tagging.transform([n])

        replace_sent = loaded_sent_vect_replaced.fit_transform(base_replace['base_sent'][0])
        tagging_sent = loaded_sent_vect_tagging.fit_transform(base_tagging['base_sent'][0])

        sent_score_replace = cosine_similarity(sent_replace, replace_sent)
        sent_score_tagging = cosine_similarity(sent_tagging, tagging_sent)
        sent_score_nng = cosine_similarity(sent_nng, tagging_sent)

        max_sent_score_nng = max(sent_score_nng.tolist()[0])
        max_sent_score_replace = max(sent_score_replace.tolist()[0])
        max_sent_score_tagging = max(sent_score_tagging.tolist()[0])

        sent_output_replace = loaded_model_sent_replaced.predict(sent_replace)
        sent_output_tagging = loaded_model_sent_tagging.predict(sent_tagging)
        sent_output_nng = loaded_model_sent_tagging.predict(sent_nng)

        if raw_text_len <int(2):
            return None
        if max_sent_score_nng == 0:
            if max_sent_score_replace == max_sent_score_tagging == 0:
                return None
            else:
                if max_sent_score_replace > max_sent_score_tagging:
                    return_checker = constrainter(senti=sent_output_replace, text=text)
                    # 제약조건, return : 제약조건에 걸리면 False, 통과하면 True

                    answer_list = self.output_DB.answers(sent_output_replace[0])

                    output = {
                        'class': sent_output_replace,
                        'reaction': answer_list[0],
                        'score': max_sent_score_replace + 0.637
                    }

                    if return_checker : return output
                    else :
                        return None
                else:

                    return_checker = constrainter(senti=sent_output_tagging, text=tagging_text)
                    if tagging_text == '너 도':
                        return None
                    # 제약조건, return : 제약조건에 걸리면 False, 통과하면 True

                    answer_list = self.output_DB.answers(sent_output_tagging[0])

                    output = {
                        'class': sent_output_tagging,
                        'reaction': answer_list[0],
                        'score': max_sent_score_tagging + 0.603
                    }

                    if return_checker : return output
                    else :
                        return None
        else:
            return_checker = constrainter(senti=sent_output_nng, text=text)
            # 제약조건, return : 제약조건에 걸리면 False, 통과하면 True
            answer_list = self.output_DB.answers(sent_output_nng[0])
            output = {
                'class': sent_output_nng,
                'reaction': answer_list[0],
                'score': max_sent_score_nng + 0.637
            }

            if return_checker: return output
            else :
                return None

    def get_chat_response(self, statement):

        _text = statement.input['text']
        response_text_reaction = self.get_reaction(_text)

        statement.output['text'] = ''
        statement.output['confidence'] = 0.0

        if response_text_reaction is not None:
            print('----------------------------------------')
            print(response_text_reaction)
            statement.output['text'] = response_text_reaction['reaction']
            statement.output['confidence'] = response_text_reaction['score']
            return statement

        return statement