import random

class QuestionIndexSelectModel() :

    def __init__(self, cursor, user_key):
        self.cursor = cursor
        self.user_key = user_key
        self.survey_group = [1]


    def select(self, user_key):
        sql = "SELECT id, question, survey_id " \
              " FROM survey_question " \
              " WHERE survey_id = 1"
        self.cursor.execute(sql)
        questions  = self.cursor.fetchall()

        question_ids = set()

        for question in questions :
            question_ids.add(question["id"])


        sql = "SELECT question_id, survey_id " \
              " FROM user_survey_question_state " \
              " WHERE survey_id = 1 and state = 1 and user_key = %s "
        self.cursor.execute(sql, (user_key))
        rows = self.cursor.fetchall()
        temp_ids = set()
        for row in rows :
            temp_ids.add(row["question_id"])

        question_ids = question_ids - temp_ids
        if len(question_ids) > 0 :
            results = list(question_ids)
            random.shuffle(results)
            return results[0]

        return None