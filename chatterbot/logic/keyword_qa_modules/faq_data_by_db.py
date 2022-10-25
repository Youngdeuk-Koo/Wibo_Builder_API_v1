import pymysql


class FAQDataDB():
    def __init__(self, conn, curs):
        self.db = conn
        self.cursor = curs
        # self.host = '54.180.88.116'
        # self.user = 'root'
        # self.passwd = '7890uiop'
        # self.dbname = 'wibo'
        #
        # self.connect()

    # def connect(self):
    #     self.db = pymysql.connect(host = self.host, user = self.user, passwd = self.passwd, db = self.dbname)
    #     self.cursor = self.db.cursor()
    #     print('connected db')


    def entity_keywords(self, chatbot_id):
        sql = "SELECT id, title, data from settings_entity where chatbot_id=%s"
        self.cursor.execute(sql, (chatbot_id))
        rs = self.cursor.fetchall()
        entitys = {}

        for row in rs:
            index = row['title'].strip()
            if index != '' :
                temps = []
                keywords = row['data'].split(",")
                for keyword in keywords :
                    keyword = keyword.strip()
                    keyword = keyword.lower()
                    temps.append(keyword)
                entitys[index] = temps
        return entitys


    def category(self, category_id):
        sql = "SELECT id, title from keywordqa_intentcategory where id=%s"
        self.cursor.execute(sql, (category_id))
        rs = self.cursor.fetchall()
        if rs is None or len(rs) == 0 :
            return None
        return {'id' : rs[0]['id'], 'title': rs[0]['title']}


    def intent_rules(self, module_id, intents):
        if intents is None or len(intents) == 0 :
            return None

        if len(intents) > 1 :
            where = ""
            for intent in intents :
                if where == "" :
                    where = 'qintents like \'%' + intent + '%\''
                else :
                    where += ' OR qintents like \'%' + intent + '%\''

        else :
            where = 'qintents like \'%' + intents[0] +  '%\''


        where = "(" + where + ")  AND kc.module_id = " + str(module_id)


        sql = "SELECT input, output, question_intent_id, ki.title as title, category_id, qintents FROM keywordqa_intent ki" \
              " INNER JOIN keywordqa_intentcategory kc on ki.category_id = kc.id WHERE " + where

        # print(sql)

        self.cursor.execute(sql)
        rs = self.cursor.fetchall()

        results = []
        for row in rs:
            keywords = row['input'].split(",")
            keywords = [keyword.strip() for keyword in keywords if len(keyword.strip()) > 0]
            question_ids = None
            if row['qintents'] is not None :
                question_ids = row['qintents'].split(",")

            is_check_intent = False
            if row['qintents'] is None :  continue

            ## like 검색은 부정확 하여 한번더 필터링 한다.
            for question_id in question_ids :
                    if question_id in intents :
                        is_check_intent = True
                        break
            if is_check_intent :
                results.append( (keywords,row['output'], row['question_intent_id'], row['title'], row['category_id'], question_ids))
        return results


    # def close(self):
    #     self.cursor.close()
    #     self.db.close()
    #     print('unconnected db')
