from chatterbot.logic import LogicAdapter
from chatterbot.utils import import_module

class CustomAdapter(LogicAdapter):
    """
    """

    def __init__(self, chatbot, **kwargs) :
        super().__init__(chatbot, **kwargs)
        self.conn, self.curs = self.chatbot.storage.get_resource()


    def get_intents(self) :
        sql = "select ci.title as title, ci.module_id as category_id, ci.output as output," \
              "  cl.title as logic_title, logic_id as logic_id  " \
              "from custom_intent as ci " \
              " inner join pipeline_custommodule cic on cic.module_ptr_id = ci.module_id " \
              " inner join custom_logic cl on cl.id = cic.logic_id " \
              " where cic.module_ptr_id = %s and cic.logic_id = %s"
        self.curs.execute(sql, (self.id, self.custom_id))
        rows = self.curs.fetchall()

        results = {}
        for row in rows :
            results[row["title"]] = row

        return results



    def select_response_format(self, text, table):
        response = str(self.select_response(response_list=text))
        response = response.format(**table)
        #response = response.replace("{p}", "%s")
        #response = response.replace("{h}", "%d")
        #response = response.replace("{m}", "%d")
        return response

