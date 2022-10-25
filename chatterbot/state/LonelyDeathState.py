#from chatterbot.state.MsgState import MsgState
from automaton import Event
from automaton import Automaton
import numpy as np


import redis


class LDOneQState(Automaton) :
    alone = Event("init", "혼자")
    alone_positive = Event("혼자", "혼자_긍정")
    alone_negative = Event("혼자", "혼자_부정")
    death = Event("혼자_부정", "죽음")
    death_positive = Event("죽음", "죽음_긍정")
    death_negative = Event("죽음", "죽음_부정")

    @property
    def is_end(self):

        if self.state == "혼자_긍정" or self.state ==  "죽음_긍정" or self.state ==  "죽음_부정":
            return True

        return False

    @property
    def is_depth_line(self):

        if self.state == "혼자_부정" :
            return True
        return False

    @property
    def accept(self):
        if self.state == "죽음_부정" :
            return True
        return False

    @property
    def score(self):
        return [-0.06, 0.66, -1.76, -0.67]

    def next_state(self, feature):

        if self.state == "init":
            return "혼자"

        if self.state == "혼자" :

            if feature == 1 :
                return "혼자_긍정"
            else :
                return "혼자_부정"

        if self.state == "죽음":
            if feature == 1:
                return "죽음_긍정"
            else:
                return "죽음_부정"

        if self.state == "혼자_부정":
            return "죽음"

        return None

    def state_tr(self, current):

        if current == "혼자" :
            return self.alone

        if current == "혼자_긍정":
            return self.alone_positive

        if current == "혼자_부정":
            return self.alone_negative

        if current == "죽음":
            return self.death

        if current == "죽음_긍정":
            return self.death_positive

        if current == "죽음_부정":
            return self.death_negative

        return None




class LDTwoQState(Automaton) :
    alone = Event("init", "혼자")
    alone_positive = Event("혼자", "혼자_긍정")
    alone_negative = Event("혼자", "혼자_부정")
    death = Event("혼자_부정", "죽음")
    death_positive = Event("죽음", "죽음_긍정")
    death_negative = Event("죽음", "죽음_부정")

    sorrow = Event("죽음_부정", "슬픔")
    sorrow_positive = Event("슬픔", "슬픔_긍정")
    sorrow_negative = Event("슬픔", "슬픔_부정")

    @property
    def is_end(self):

        if self.state == "혼자_긍정" or self.state ==  "죽음_긍정" or self.state ==  "슬픔_긍정" or self.state ==  "슬픔_부정":
            return True

        return False

    @property
    def is_depth_line(self):

        if self.state == "혼자_부정"  or self.state == "죽음_부정" :
            return True
        return False

    @property
    def accept(self):
        if self.state == "슬픔_부정" :
            return True
        return False

    @property
    def score(self):
        return [-0.41, 0.53, -0.41, 1.37]

    def next_state(self, feature):

        if self.state == "init":
            return "혼자"

        if self.state == "혼자" :

            if feature == 1 :
                return "혼자_긍정"
            else :
                return "혼자_부정"


        if self.state == "혼자_부정":
            return "죽음"

        if self.state == "죽음":
            if feature == 1:
                return "죽음_긍정"
            else:
                return "죽음_부정"

        if self.state == "죽음_부정":
            return "슬픔"

        if self.state == "슬픔":
            if feature == 1:
                return "슬픔_긍정"
            else:
                return "슬픔_부정"

        return None

    def state_tr(self, current):

        if current == "혼자" :
            return self.alone

        if current == "혼자_긍정":
            return self.alone_positive

        if current == "혼자_부정":
            return self.alone_negative

        if current == "죽음":
            return self.death

        if current == "죽음_긍정":
            return self.death_positive

        if current == "죽음_부정":
            return self.death_negative

        if current == "슬픔":
            return self.sorrow

        if current == "슬픔_긍정":
            return self.sorrow_positive

        if current == "슬픔_부정":
            return self.sorrow_negative

        return None


class LDeathMsgStateFlow():

    def __init__(self, cache_store, user_key, cur):
        self.r = cache_store
        self.user_key = user_key
        self.cur = cur
        self.pre_state = None


        self.msg_map = {}

        self.msg_map[1] = LDOneQState
        self.msg_map[2] = LDTwoQState

    def get_pre_state(self):
        self.pre_state = self.r.get(self.user_key + '_survey_state')
        return self.pre_state

    def get_pre_index(self):
        survey_index = self.r.get(self.user_key + '_survey_index')
        if survey_index is None :
            return None

        return int(survey_index)

    def start(self, msg_index):

        self.msg_index = msg_index

        print("msg_type : ", type(self.msg_index))

        if self.pre_state is None :
            self.pre_state = self.get_pre_state()

        if self.msg_index in self.msg_map :
            if self.pre_state is not None :
                self.questionState = self.msg_map[self.msg_index](initial_state=self.pre_state)
            else :
                self.questionState = self.msg_map[self.msg_index](initial_state="init")


        print("pre_state", self.pre_state)

        print(self.questionState.state)


    def next_state(self, feature):
        return self.questionState.next_state(feature)

    @property
    def state(self):
        return self.questionState.state


    @property
    def is_depth_line(self):
        return self.questionState.is_depth_line

    def save_state(self):

        print("===> is end", self.questionState.is_end)

        if self.questionState.is_end :
            self.r.delete(self.user_key + '_survey_state')
            self.r.delete(self.user_key + '_survey_index')
            sql = "insert into user_survey_question_state(user_key, survey_id, question_id, state)VALUES(%s, 1, %s, 1) "
            self.cur.execute(sql, (self.user_key, str(self.msg_index)))

            if self.questionState.accept :
                score = self.questionState.score
                index  = np.argmax(score)
                sql = "insert into user_survey_score(user_key, score, survey_id, class)" \
                      "VALUES(%s, %s, 1, %s) " \
                      " ON DUPLICATE KEY UPDATE score=score + %s"
                self.cur.execute(sql, (self.user_key, str(score[index]), str(index + 1), str(score[index])))

        else :
            self.r.set(self.user_key + '_survey_state', self.questionState.state)
            self.r.set(self.user_key + '_survey_index', self.msg_index)
        #self.stack.append()


    def transition(self, state):
        tr = self.questionState.state_tr(state)
        tr()
