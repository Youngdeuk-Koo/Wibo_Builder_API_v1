import pymysql
import random

class OutputByDB():
    def __init__(self):
        self.host = '54.180.88.116'
        self.user = 'mrmind'
        self.passwd = 'mrmind0610@!'
        self.dbname = 'nlp_data'

        self.connect()

    def connect(self):
        self.db = pymysql.connect(host = self.host, user = self.user, passwd = self.passwd, db = self.dbname)
        self.cursor = self.db.cursor()
        print('connected db')

    def answers(self, sentiment):
        sql = "SELECT response from intent_response where sentiment=%s"
        self.cursor.execute(sql, (sentiment))
        rs = self.cursor.fetchall()
        answer_list = []
        for row in rs:
            answer_list.append(row[0])
        random.shuffle(answer_list)
        #print(answer_list[0])

        return answer_list

    def close(self):
        self.cursor.close()
        self.db.close()
        print('unconnected db')
