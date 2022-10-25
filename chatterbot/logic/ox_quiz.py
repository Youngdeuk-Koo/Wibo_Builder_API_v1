from chatterbot.logic import LogicAdapter
from chatterbot import response_selection
from chatterbot.comparisons import levenshtein_distance

import json


class OXQuizAdapter(LogicAdapter):
    
    DICT_PATH = "chatterbot/logic/ox_quiz/"

    dict_intents = json.load(open(DICT_PATH+"intents.json"))
    dict_entities = json.load(open(DICT_PATH+"entities.json"))
    dict_qa = json.load(open(DICT_PATH+"qa.json"))
    dict_response = json.load(open(DICT_PATH+"response.json"))


    def can_process(self, statement):
        return True

    def process(self, statement, intent=None):

        curr_card_id = self.get_curr_card(statement)

        if intent is None:
            intent, confidence = self.recognize_intent(statement)
        else:
            confidence = 1.0

        # 퀴즈 요청 
        if intent == "request_quiz":
            if curr_card_id is None:
                statement = self.get_initial_message(statement)
                quiz_key, quiz = self.get_randum_quiz(statement)
                statement.context['ox_quiz']['curr_card'] = quiz_key
                statement.context['ox_quiz']['question_cnt'] += 1

                _text = self.get_quiz_text(quiz['question'])
                statement.output.append({"text": _text})
                statement.result['module'].insert(0, self.title)
                statement.result['intent'].insert(0, intent)
                statement.result['confidence'] = 1.0
            else:
                quiz = self.dict_qa[curr_card_id]

                _text = self.get_quiz_text(quiz['question'])
                statement.output.append({"text": _text})
                statement.result['module'].insert(0, self.title)
                statement.result['intent'].insert(0, intent)
                statement.result['confidence'] = 1.0


        # 다른 퀴즈 요청
        elif intent == "request_other_quiz" and curr_card_id is not None:
            quiz = self.dict_qa[curr_card_id]

            # 정답 확인 완료
            if len(self.dict_qa.keys()) - 1 == len(statement.context['ox_quiz']['stack']):
                statement.context['ox_quiz']['stack'] = []
            statement.context['ox_quiz']['stack'].append(curr_card_id)

            new_quiz_key, new_quiz = self.get_randum_quiz(statement)
            statement.context['ox_quiz']['curr_card'] = new_quiz_key
            statement.context['ox_quiz']['question_cnt'] += 1

            _text = self.get_other_quiz_text(quiz['answer'], quiz['description'], new_quiz['question'])
            statement.output.append({"text": _text})
            statement.result['module'].insert(0, self.title)
            statement.result['intent'].insert(0, intent)
            statement.result['confidence'] = 1.0


        # 퀴즈 다시 듣기 요청
        elif intent == "repeat_quiz" and curr_card_id is not None:
            quiz = self.dict_qa[curr_card_id]

            _text = self.get_repeat_quiz_text(quiz['question'])
            statement.output.append({"text": _text})
            statement.result['module'].insert(0, self.title)
            statement.result['intent'].insert(0, intent)
            statement.result['confidence'] = 1.0

        # 퀴즈 놀이 멈춤
        elif intent == "stop_quiz" and curr_card_id is not None:

            _text = self.get_stop_quiz_text()
            statement.output.append({"text": _text})
            statement.result['module'].insert(0, self.title)
            statement.result['intent'].insert(0, intent)
            statement.result['confidence'] = 1.0

            del statement.context['ox_quiz']

        else:
            if curr_card_id is None:
                return statement

            # 정답 확인
            quiz = self.dict_qa[curr_card_id]
            result = self.check_answer(statement)

            if result is None:
                statement.context['ox_quiz']['else_cnt'] += 1
                if statement.context['ox_quiz']['else_cnt'] >= 2:
                    del statement.context['ox_quiz']
                    _text = self.get_auto_stop_quiz_text()
                else:
                    _text = self.get_quiz_answer_else_text(quiz['question'])

                statement.output.append({"text": _text})
                statement.result['module'].insert(0, self.title)
                statement.result['intent'].insert(0, intent)
                statement.result['confidence'] = 1.0

                return statement

            if len(self.dict_qa.keys()) - 1 == len(statement.context['ox_quiz']['stack']):
                statement.context['ox_quiz']['stack'] = []
            statement.context['ox_quiz']['stack'].append(curr_card_id)
            _text = self.get_quiz_answer_text(result, quiz['answer'], quiz['description'])
            if result: statement.context['ox_quiz']['answer_cnt'] += 1

            if statement.context['ox_quiz']['question_cnt'] >= 1:
                _score = self.get_total_result_score(statement)
                _text = self.get_quiz_result_text(_score, _text)
                del statement.context['ox_quiz']

            else:
                #  다음 문제
                new_quiz_key, new_quiz = self.get_randum_quiz(statement)
                statement.context['ox_quiz']['curr_card'] = new_quiz_key
                statement.context['ox_quiz']['question_cnt'] += 1
                _text = self.get_next_quiz_text(_text, new_quiz['question'])

            statement.output.append({"text": _text})
            statement.result['module'].insert(0, self.title)
            statement.result['intent'].insert(0, intent)
            statement.result['confidence'] = 1.0

        return statement


    def get_curr_card(self, statement):
        if 'ox_quiz' in statement.context:
            if int(statement.context['ox_quiz']['curr_card']) > 0:
                return statement.context['ox_quiz']['curr_card']
        return None


    def recognize_intent(self, statement):
        input_text = statement.input['text'].replace(' ', '')
        input_text = self.recognize_entity(input_text)

        for intent, _samples in self.dict_intents.items():
            for sample in _samples:
                _confidence = self.compare_statements(input_text, sample.replace(' ', ''))
                if sample.startswith('['):
                    if _confidence == 1.0:
                        return intent, _confidence
                else:
                    if _confidence > 0.7:
                        return intent, _confidence
        return None, 0.0


    def recognize_entity(self, input_text):
        def window(fseq, window_size=5):
            for i in range(len(fseq) - window_size + 1):
                start = i
                end = i + window_size
                yield fseq[start:end]

        for _entity_title, _entity_items in self.dict_entities.items():
            for _item in _entity_items:
                _tmp_item = _item.replace(' ', '')
                for _seq in window(input_text, len(_tmp_item)):
                    _confidence = levenshtein_distance(_tmp_item, _seq)
                    if _confidence > 0.8:
                        return input_text.replace(_seq, '@' + _entity_title)
        return input_text


    def get_initial_message(self, statement):
        if 'ox_quiz' not in statement.context:
            statement.context['ox_quiz'] = {
                'stack': [],
                'curr_card': -1,
                'question_cnt': 0,
                'answer_cnt': 0,
                'else_cnt': 0
            }
        return statement
    
    
    def get_randum_quiz(self, statement):
        _keys = self.dict_qa.keys()
        _keys = list(set(_keys) - set(statement.context['ox_quiz']['stack']))
        _key = response_selection.get_random_response(response_list=_keys)
        return _key, self.dict_qa[_key]
    

    def check_answer(self, statement):
        sample_o = [
        "오","o", "O", "오오", "오후", "맞아", "동그라미", "동구라미" , "똥구라미", "똥그라미", "오야", "오후" , "보" , "고", "어", "오전", "오 오", "정담은 오", "후 후 후", "후 후 후 후", "어 어",  "정답은 5", "오 오 오", "오지", "어 어 어"
        ]
        sample_x = [
        "x", "X", "엑스", "엑쓰", "엑스야", "틀렸어", "틀려", "아니야", "아냐", "xx", "팩스", "엑수", "액수", "xg","액트", "섹스", "앱스", "s", "엑소", "s", "f", "빅스", "깼어", "엑스 엑스 엑스", "엑스 엑스야", "악수", "엑서", "정답은 X"
        ]

        # sample_o = ["오", "o", "O", "오오", "맞아", "동그라미", "오야", "오후", "고", "오예", "어", "응"]
        # sample_x = ["x", "X", "엑스", "엑쓰", "엑스야", "틀렸어", "틀려", "아니야", "아냐", "xx", "팩스", "엑수", "액수"]
        input_text = statement.input['text'].replace(' ', '')
        in_ans = None

        curr_card_id = self.get_curr_card(statement)
        if curr_card_id is None:
            return None

        ans = self.dict_qa[curr_card_id]['answer']

        if input_text.strip() in sample_o:
            in_ans = 'O'
        elif input_text.strip() in sample_x:
            in_ans = 'X'

        print('check_answer', in_ans)

        if in_ans is not None:
            if in_ans == ans:
                return True
            else:
                return False

        return None
    
    
    def get_total_result_score(self, statement):
        question_cnt = statement.context['ox_quiz']['question_cnt']
        answer_cnt = statement.context['ox_quiz']['answer_cnt']
        try:
            score = question_cnt/answer_cnt
        except ZeroDivisionError:
            score = 0

        return score
    

    def get_quiz_text(self, text):
        return response_selection.get_random_response(response_list=self.dict_response['intro_first_quiz']) \
               + " " + text + " " \
               + response_selection.get_random_response(response_list=self.dict_response['quide_quiz'])

    def get_quiz_text_else(self, text):
        return response_selection.get_random_response(response_list=self.dict_response['intro_dbl_req_quiz']) \
               + " " + text + " " \
               + response_selection.get_random_response(response_list=self.dict_response['quide_quiz'])

    def get_other_quiz_text(self, _answer, _desc, _question):
        _answer = '정답은 ' + _answer
        return response_selection.get_random_response(response_list=self.dict_response['intro_other_quiz']) \
               + " " + _answer + ", " + _desc + " " \
               + response_selection.get_random_response(response_list=self.dict_response['intro_next_quiz']) \
               + " " + _question + " " \
               + response_selection.get_random_response(response_list=self.dict_response['quide_quiz'])

    def get_next_quiz_text(self, _text, _question):
        return _text + " " \
               + response_selection.get_random_response(response_list=self.dict_response['intro_next_quiz']) \
               + " " + _question + " " \
               + response_selection.get_random_response(response_list=self.dict_response['quide_quiz'])

    def get_quiz_result_text(self, _score, _text):
        if _score == 1:
            sample = self.dict_response['result_score_100']
        elif _score > 0.5:
            sample = self.dict_response['result_score_50_more']
        elif _score > 0:
            sample = self.dict_response['result_score_50_less']
        else:
            sample = self.dict_response['result_score_0']
        return _text + " " + response_selection.get_random_response(response_list=sample)

    def get_repeat_quiz_text(self, text):
        return response_selection.get_random_response(response_list=self.dict_response['intro_repeat_quiz']) \
               + " " + text + " " \
               + response_selection.get_random_response(response_list=self.dict_response['quide_quiz'])

    def get_quiz_answer_text(self, _result, _answer, _desc):
        _answer = '정답은 ' + _answer
        _text = ''
        if _result:
            _text += response_selection.get_random_response(response_list=self.dict_response['result_answer_success'])
        else:
            _text += response_selection.get_random_response(response_list=self.dict_response['result_answer_fail'])
        _text += ' ' + _answer + ', ' + _desc
        return _text

    def get_quiz_answer_else_text(self, _question):
        return response_selection.get_random_response(response_list=self.dict_response['intro_quiz_else']) \
               + " " + _question + " " \
               + response_selection.get_random_response(response_list=self.dict_response['quide_quiz'])

    def get_stop_quiz_text(self):
        return response_selection.get_random_response(response_list=self.dict_response['guide_stop_quiz'])

    def get_auto_stop_quiz_text(self):
        return response_selection.get_random_response(response_list=self.dict_response['guide_auto_stop_quiz'])
