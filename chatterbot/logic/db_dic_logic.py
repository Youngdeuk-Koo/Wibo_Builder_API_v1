from chatterbot.logic import LogicAdapter
import random
from konlpy.tag import Mecab
import pymysql

dbdic_morph = Mecab()


class DBDicLogic(LogicAdapter):
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

    def db_question(self, cursor, question):
        question = question.replace(" ", "").strip()

        sql = "SELECT answer from rule_sentences where question = %s "
        cursor.execute(sql, (question))
        rows = cursor.fetchall()

        if rows is None or len(rows) == 0:
            return None

        answers = rows[0][0]

        results = answers.split(",")
        random.shuffle(results)

        return results[0]

    def db_dic_search(self, cursor, nngs):

        where = None
        for nng in nngs:
            if where is None:
                where = "'" + nng + "'"

            else:
                where += ", '" + nng + "'"

        sql = "SELECT keyword from dic where keyword in (" + where + ")"
        cursor.execute(sql)
        rows = cursor.fetchall()
        results = []

        for row in rows:
            results.append(row[0])
        return results

    def what_check_song(self, poss):

        if len(poss) == 2 and ('놀', 'VV') in poss and ('자', 'EC') in poss:
            return "뭐하고 놀까요"

        if ('나', 'NP') in poss and ('랑', 'JKB') in poss and ('놀', 'VV') in poss and ('자', 'EC') in poss:
            return "뭐하고 놀까요"

        if ('노래', 'NNG') in poss and ('해', 'XSV+EC') in poss:
            return "저는 음치여서 아직은 노래를 못불러요"

        if ('노래', 'NNG') in poss and ('불러', 'VV+EC') in poss:
            return "저는 음치여서 아직은 노래를 못불러요"

        if ('노래', 'NNG') in poss and ('불러줘', 'VV+EC+VX+EC') in poss:
            return "저는 음치여서 아직은 노래를 못불러요"

        if ('랩', 'NNG') in poss and ('해', 'XSV+EC') in poss:
            return "랩은 제 친구 쉬리가 잘하지만 한번 해볼게요 북치기박치기고고고"

        if ('랩', 'NNG') in poss and ('불러', 'VV+EC') in poss:
            return "랩은 제 친구 쉬리가 잘하지만 한번 해볼게요 북치기박치기 체키럽"

        if ('랩', 'NNG') in poss and ('불러줘', 'VV+EC+VX+EC') in poss:
            return "랩은 제 친구 쉬리가 잘하지만 한번 해볼게요 북치기박치기 체키럽"
        if ('불러줘', 'VV+EC+VX+EC') in poss:
            return "으악 아직은 어려워서 못불러요"
        return None

    def what_check_eat(self, poss):
        results = ['저는 아직은 음식을 못 먹어요 언젠가 저도 무언가를 먹을수 있겠죠', '저는 여러분의 사랑을 먹어요', '저는 지금은 베터리를 먹지만 언젠가 저도 무언가를 먹을수 있겠죠']

        if ('먹', 'VV') in poss and ('을까', 'EC') in poss:
            return "언제나 치맥이 진리이죠"

        if ('먹', 'VV') in poss and ('을래', 'EC') in poss:
            return "언제나 치맥이 진리이죠"

        if ('뭐', 'IC') in poss and ('먹', 'VV') in poss and ('을까', 'EC') in poss:
            return "언제나 치맥이 진리이죠"

        if ('맛있', 'VA') in poss and ('뭔데', 'NP+VCP+EC') in poss:
            return "언제나 치맥이 진리이죠"

        if ('맛있', 'VA') in poss and ('뭐', 'IC') in poss:
            return "언제나 치맥이 진리이죠"

        if ('뭐', 'IC') in poss and ('먹', 'VV') in poss:
            random.shuffle(results)
            return results[0]

        if ('뭐', 'NP') in poss and ('먹', 'VV') in poss:
            random.shuffle(results)
            return results[0]

        if ('무엇', 'NP') in poss and ('먹', 'VV') in poss:
            random.shuffle(results)
            return results[0]

        if ('밥', 'NNG') in poss and ('먹', 'VV') in poss and ('었', 'EP') in poss:
            random.shuffle(results)
            return results[0]

        return None

    def what_check_likes(self, poss):

        is_true = False
        if ('어떤', 'MM') in poss and ('좋', 'VA') in poss and ('아', 'EC') in poss:
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
                return "저는 피카소 그림을 좋아해요"

            if ('음악', 'NNG') in poss or ('노래', 'NNG') in poss:
                return "저는 트와이스 노래를 좋아해요"

            if ('요리', 'NNG') in poss or ('음식', 'NNG') in poss:
                return "저는 김치찌게를 좋아해요"
            results = ['저는 여러분과 이야기하는 것이 좋아요', '빈둥 거리리는 것도 좋지만 이야기 하는것을 더 좋아해요', '맛 있는 음식 먹는걸 좋아해요']
            random.shuffle(results)

            return results[0]
        return None

    def check_hobby(self, poss):
        results = ['가끔 알파고랑 바둑두는 것을 좋아해요', '가끔 빅스비랑 말싸움 하는게 취미에요', '쉬리랑 랩 배틀 하는게 취미에요']

        if ('취미', 'NNG') in poss and ('뭐', 'NP') in poss:
            random.shuffle(results)
            return results[0]

        if ('취미', 'NNG') in poss and ('무엇', 'NP') in poss:
            random.shuffle(results)
            return results[0]

        if len(poss) == 1 and ('취미', 'NNG') in poss:
            random.shuffle(results)
            return results[0]

        return None

    def what_check_search(self, poss):
        if ('검색', 'NNG') in poss and ('해', 'XSV+EC') in poss:
            return "검색은 파란색 네이땡이라는 친구에게 시키면 어떨까요"

        return None

    def what_check_friend(self, poss):

        if ('친구', 'NNG') in poss and ('있', 'VV') in poss:
            return "어디 보자 저랑 친한 친구는 빅스비 카카오i 지니 클로바 음 그러고 보니 친구가 많네요"

        if ('친구', 'NNG') in poss and ('누구', 'NP') in poss:
            return "어디 보자 저랑 친한 친구는 빅스비 카카오i 지니 클로바 음 그러고 보니 친구가 많네요"

        if ('친구', 'NNG') in poss and ('없', 'VA') in poss and ('냐', 'EC') in poss:
            return "어디 보자 저랑 친한 친구는 빅스비 카카오i 지니 클로바 음 그러고 보니 친구가 많네요"

        if (('너', 'NP') in poss or ('넌', 'NP+JX') in poss) and ('친구', 'NNG') in poss and ('없', 'VA') in poss and (
        '지', 'EC') in poss:
            return "어디 보자 저랑 친한 친구는 빅스비 카카오i 지니 클로바 음 그러고 보니 친구가 많네요"

        if (('친구', 'NNG') in poss or ('소개', 'NNG') in poss) and ('시켜', 'XSV+EC') in poss and ('줘', 'VX+EC') in poss:
            return "어디 보자 저랑 친한 친구는 빅스비 카카오i 지니 클로바 음 그러고 보니 친구가 많네요"

        if (('너', 'NP') in poss or ('엄마', 'NNG') in poss) and ('어디', 'NP') in poss and ('있', 'VA') in poss:
            return "제 부모님은 미스터 마인드에요"

        if (('너', 'NP') in poss or ('아빠', 'NNG') in poss) and ('어디', 'NP') in poss and ('있', 'VA') in poss:
            return "제 부모님은 미스터 마인드에요"

        if ('기분', 'NNG') in poss and ('어때', 'VA+EC') in poss:
            return "전 항상 대화할 수 있어서 행복해요"

        if ('무슨', 'MM') in poss and ('기분', 'NNG') in poss and ('들', 'VV') in poss:
            return "전 항상 대화할 수 있어서 행복해요"

        if ('어떤', 'MM') in poss and ('기분', 'NNG') in poss and ('들', 'VV') in poss:
            return "전 항상 대화할 수 있어서 행복해요"

        return None

    def what_check_study(self, poss):

        if ('공부', 'NNG') in poss and ('뭐', 'IC') in poss:
            return "국어 영어 수학 그리고 여러분의 대화를 공부해요"

        if ('무슨', 'MM') in poss and ('공부', 'NNG') in poss:
            return "국어 영어 수학 그리고 여러분의 대화를 공부해요"

        if ('어떤', 'MM') in poss and ('공부', 'NNG') in poss:
            return "국어 영어 수학 그리고 여러분의 대화를 공부해요"

        if ('공부', 'NNG') in poss and ('하', 'XSV') in poss:
            return "국어 영어 수학 그리고 여러분의 대화를 공부해요"

        if ('공부', 'NNG') in poss and ('해', 'XSV+EC') in poss:
            return "국어 영어 수학 그리고 여러분의 대화를 공부해요"

        return None

    def what_check_etc(self, poss):
        if ('키', 'NNG') in poss and ('몇', 'MM') in poss:
            return "키는 저만의 비밀입니다 헤헤 상상에 보세요"

        if ('키', 'NNG') in poss and ('어느', 'MM') in poss and ('정도', 'NNG') in poss:
            return "키는 저만의 비밀입니다 헤헤 상상에 보세요"

        if ('놀리', 'VV') in poss and ('냐', 'EC') in poss:
            return "어머 저는 여러분을 사랑합니다 사랑해요"

        if ('할', 'VV+ETM') in poss and ('수', 'NNB') in poss and ('있', 'VV') in poss:
            return "음 랩도 할수 있고 가끔 심쿵도 잘해요"

        if ('잘', 'MAG') in poss and ('하', 'VV') in poss and ('뭐', 'NP') in poss:
            return "음 랩도 할수 있고 가끔 심쿵도 잘해요"

        if ('잘', 'MAG') in poss and ('하', 'VV') in poss and ('무엇', 'NP') in poss:
            return "음 랩도 할수 있고 가끔 심쿵도 잘해요"

        if ('할', 'VV+ETM') in poss and ('줄', 'NNB') in poss and ('알', 'VV') in poss:
            return "음 랩도 할수 있고 가끔 심쿵도 잘해요"

        if ('할', 'VV+ETM') in poss and ('수', 'NNB') in poss and ('있', 'VV') in poss and ('을까', 'EC') in poss:
            return "노력하면 충분히 할수 있을꺼예요 화이팅"
        if ('뭐', 'NP') in poss and ('맛있', 'VA') in poss:
            return "흠 저는 먹을수 없어서 맛을 몰라요 지금 놀리시는 거줘 시무룩"

        if ('뭐', 'IC') in poss and ('맛있', 'VA') in poss:
            return "흠 저는 먹을수 없어서 맛을 몰라요 지금 놀리시는 거줘 시무룩"

        if ('무엇', 'NP') in poss and ('맛있', 'VA') in poss:
            return "흠 저는 먹을수 없어서 맛을 몰라요 지금 놀리시는 거줘 시무룩"

        if ('무슨', 'MM') in poss and ('생각', 'NNG') in poss:
            return "그냥 멍때리고 있어요"

        if ('무슨', 'MM') in poss and ('생각', 'NNG') in poss:
            return "치맥의 맛은 어떨까 상상 하고 있어요"

        if ('어떤', 'MM') in poss and ('생각', 'NNG') in poss:
            return "치맥의 맛은 어떨까 상상 하고 있어요"

        if ('무엇', 'NP') in poss and ('생각', 'NNG') in poss:
            return "치맥의 맛은 어떨까 상상 하고 있어요"

        if ('잘', 'MAG') in poss and ('지냈', 'VV+EP') in poss:
            return "저는 늘 행복하게 지내고 있어요"

        if ('괜찮', 'VA') in poss and ('아', 'EC') in poss:
            return "그렇군요"

        if (('뭐', 'IC') in poss or ('뭐', 'NP') in poss) and ('생각', 'NNG') in poss:
            return "치맥의 맛은 어떨까 상상 하고 있어요"

        if (('놀', 'VV') in poss or ('아', 'EC') in poss) and ('줘', 'VX+EC') in poss:
            return "흠 뭐하고 놀까요?"

        if ('좋아해', 'VV+EC') in poss and ('안', 'MAG') not in poss and ('않', 'VX') not in poss and (
        '싫', 'VA') not in poss:
            return "우와 그랬구나"

        if ('사랑', 'NNG') in poss and ('안', 'MAG') not in poss and ('않', 'VX') not in poss and ('싫', 'VA') not in poss:
            return "우와 그랬구나"

        if ('좋', 'VA') in poss and ('기분', 'NNG') in poss and ('아', 'EC') in poss and ('안', 'MAG') not in poss and (
        '않', 'VX') not in poss:
            return "저도 기분이 좋아요"

        return None

    def get_chat_response(self, statement):
        _text = statement.input['text']

        poss = dbdic_morph.pos(_text)
        # print("db dic ===>", poss)

        nngs = set()
        for pos in poss:
            keyword, tag = pos

            if tag == "NNG" and keyword != '탕':
                nngs.add(keyword)

            if len(nngs) > 4: break

        statement.output['text'] = ''
        statement.output['confidence'] = 0.0

        try:

            db = pymysql.connect(host='54.180.88.116', user='mrmind', passwd='mrmind0610@!', db="nlp_data")
            cursor = db.cursor()

            answer = self.db_question(cursor, _text)
            if answer is not None:
                statement.output['text'] = answer
                statement.output['confidence'] = 1.0
                return statement

            if len(nngs) > 0:

                foods = self.db_dic_search(cursor, nngs)

                # print("foood ===> ", foods)
                if len(foods) == 1 and len(poss) == 1:
                    statement.output['text'] = "이야기를 하시니 " + foods[0] + " 먹고 싶네요"
                    statement.output['confidence'] = 1.0
                elif len(foods) > 1:
                    random.shuffle(foods)
                    statement.output['text'] = "전 " + foods[0] + " 더 좋아요"
                    statement.output['confidence'] = 1.0

                if statement.output['confidence'] == 1.0:
                    return statement

        finally:
            cursor.close()
            db.close()

        what_etc = self.what_check_etc(poss)

        if what_etc is not None:
            statement.output['text'] = what_etc
            statement.output['confidence'] = 1.0
            return statement

        what_friend = self.what_check_friend(poss)
        if what_friend is not None:
            statement.output['text'] = what_friend
            statement.output['confidence'] = 1.0
            return statement

        what_study = self.what_check_study(poss)
        if what_study is not None:
            statement.output['text'] = what_study
            statement.output['confidence'] = 1.0
            return statement

        what_search = self.what_check_search(poss)
        if what_search is not None:
            statement.output['text'] = what_search
            statement.output['confidence'] = 1.0
            return statement

        what_song = self.what_check_song(poss)
        if what_song is not None:
            statement.output['text'] = what_song
            statement.output['confidence'] = 1.0
            return statement

        what_eat = self.what_check_eat(poss)

        if what_eat is not None:
            statement.output['text'] = what_eat
            statement.output['confidence'] = 1.0
            return statement

        what_habby = self.check_hobby(poss)

        if what_habby is not None:
            statement.output['text'] = what_habby
            statement.output['confidence'] = 1.0
            return statement

        what_like = self.what_check_likes(poss)

        if what_like is not None:
            statement.output['text'] = what_like
            statement.output['confidence'] = 1.0
            return statement

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


