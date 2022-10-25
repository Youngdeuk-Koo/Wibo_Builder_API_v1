
import pymysql
import re

from chatterbot.storage import StorageAdapter


class MariaDatabaseAdapter(StorageAdapter):

    def __init__(self, **kwargs):
        super(MariaDatabaseAdapter, self).__init__(**kwargs)
        self.conn = pymysql.connect(host='52.79.81.100', port=3306,
                             user='root', passwd='7890uiop', db='wibo_local', charset='utf8')
                            #  user='root', passwd='7890uiop', db='koowiboe', charset='utf8')
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)


    """
    Pipeline functions
    """
    def get_modules(self, chatbot_id):
        sql = "select * from wibo_module where chatbot_id=%s and is_enabled=%s order by position, custom_position"
        self.curs.execute(sql, (chatbot_id, 1))
        rows = self.curs.fetchall()
        return rows


    """
    Dialogflow functions
    """

    def get_dlgf_node_for_graph(self, graph_id, node_id):
        sql = "select " \
              "g.id as graph_id, g.text as graph_text, " \
              "n.id as node_id, n.key as node_key, n.type as node_type, n.text as node_text, n.max_visit_count as node_max_visit_count " \
              "from dialogflow_graph as g, dialogflow_intentnode as n " \
              "where g.id=%s and g.is_enabled=1 and n.graph_id=g.id and n.id=%s "
        self.curs.execute(sql, (graph_id, node_id, ))
        row = self.curs.fetchone()
        return row

    def get_dlgf_root_nodes_for_module(self, module_id):
        sql = "select " \
              "  g.id as graph_id, g.text as graph_text, " \
              "  n.id as node_id, n.key as node_key, n.type as node_type, n.text as node_text, n.max_visit_count as node_max_visit_count " \
              "from dialogflow_graph as g, dialogflow_intentnode as n " \
              "where n.graph_id=g.id and n.type=%s and g.module_id=%s and g.is_enabled=1 order by g.position"

        # if graph_id is not None:
        #     sql += "and g.id!=" + graph_id
        #
        # sql += " order by g.position"

        self.curs.execute(sql, ('R', module_id, ))
        rows = self.curs.fetchall()
        return rows

    def get_dlgf_next_nodes(self, node_key):
        sql = "select " \
              "  n.id as node_id, n.key as node_key, n.text as node_text , lg.id as group_id, l.id, l.type, l.sim_threshold, l.inputs_relation, l.inputs, l.inputs_pos " \
              "from dialogflow_intentnode as n, dialogflow_edge as e, dialogflow_logicgroup as lg, dialogflow_logic as l " \
              "where n.key=e.node_to and e.node_from=%s and n.id=lg.intent_id and lg.id=l.logic_group_id " \
              "order by n.id, lg.id, l.id"
        self.curs.execute(sql, (node_key, ))
        rows = self.curs.fetchall()

        nodes = []

        curr_node_id = -1
        curr_group_id = -1
        for idx, row in enumerate(rows):

            if idx == 0:
                curr_node_id = row['node_id']
                node = {
                    'id': row['node_id'],
                    'key': row['node_key'],
                    'text': row['node_text'],
                    'data': []
                }
                curr_group_id = row['group_id']
                group = {
                    'id': row['group_id'],
                    'data': []
                }

            if curr_group_id != row['group_id']:
                curr_group_id = row['group_id']
                node['data'].append(group)
                group = {
                    'id': row['group_id'],
                    'data': []
                }

            if curr_node_id != row['node_id']:
                curr_node_id = row['node_id']
                nodes.append(node)
                node = {
                    'id': row['node_id'],
                    'key': row['node_key'],
                    'text': row['node_text'],
                    'data': []
                }

            item = {
                'id': row['id'],
                'type': row['type'],
                'sim_threshold': row['sim_threshold'],
                'inputs_relation': row['inputs_relation'],
                'inputs': row['inputs'],
                'inputs_pos': row['inputs_pos']
            }

            group['data'].append(item)

            if idx == len(rows)-1:
                node['data'].append(group)
                nodes.append(node)

        return nodes

    def get_dlgf_next_nodes_cnt(self, node_key):
        sql = "select count(*) as cnt from dialogflow_edge where node_from=%s"
        self.curs.execute(sql, (node_key, ))
        row = self.curs.fetchone()
        return int(row['cnt'])

    def has_dlgf_re_visit_response(self, node_id):
        sql = "select count(*) as cnt from dialogflow_responsegroup as rg where rg.intent_id=%s and rg.condition=%s"
        self.curs.execute(sql, (node_id, 're_visit', ))
        row = self.curs.fetchone()
        return True if int(row['cnt']) > 0 else False

    def has_dlgf_last_visit_response(self, node_id):
        sql = "select count(*) as cnt from dialogflow_responsegroup as rg where rg.intent_id=%s and rg.condition=%s"
        self.curs.execute(sql, (node_id, 'last_visit', ))
        row = self.curs.fetchone()
        return True if int(row['cnt']) > 0 else False

    def get_dlgf_response_groups(self, node_id, condition='default'):
        sql = "select rg.id as group_id, r.id, r.type, r.outputs, r.custom_module_id, r.custom_module_intent_id, r.position " \
              "from dialogflow_responsegroup as rg, dialogflow_response as r " \
              "where rg.intent_id=%s and rg.condition=%s and rg.id=r.response_group_id order by rg.intent_id, r.response_group_id, r.position  "
        self.curs.execute(sql, (node_id, condition, ))
        rows = self.curs.fetchall()
        return self.get_response_groups(rows)


    """
    Dialog functions
    """
    def get_dlg_intent_nodes(self, module_id):

        sql = "select " \
              "  n.id as node_id, n.text as node_text, lg.id as group_id, l.id, l.type, l.sim_threshold, l.inputs_relation, l.inputs, l.inputs_pos " \
              "from dialog_intentnode as n, dialog_logicgroup as lg, dialog_logic as l " \
              "where n.type='I' and n.module_id=%s and n.id=lg.intent_id and lg.id=l.logic_group_id " \
              "order by n.position_code, lg.id, l.id"
        self.curs.execute(sql, (module_id, ))
        rows = self.curs.fetchall()

        nodes = []

        curr_node_id = -1
        curr_group_id = -1
        for idx, row in enumerate(rows):

            if idx == 0:
                curr_node_id = row['node_id']
                node = {
                    'id': row['node_id'],
                    'text': row['node_text'],
                    'data': []
                }
                curr_group_id = row['group_id']
                group = {
                    'id': row['group_id'],
                    'data': []
                }

            if curr_group_id != row['group_id']:
                curr_group_id = row['group_id']
                node['data'].append(group)
                group = {
                    'id': row['group_id'],
                    'data': []
                }

            if curr_node_id != row['node_id']:
                curr_node_id = row['node_id']
                nodes.append(node)
                node = {
                    'id': row['node_id'],
                    'text': row['node_text'],
                    'data': []
                }

            item = {
                'id': row['id'],
                'type': row['type'],
                'sim_threshold': row['sim_threshold'],
                'inputs_relation': row['inputs_relation'],
                'inputs': row['inputs'],
                'inputs_pos': row['inputs_pos']
            }

            group['data'].append(item)

            if idx == len(rows) - 1:
                node['data'].append(group)
                nodes.append(node)

        return nodes

    def get_dlg_response_groups(self, node_id):

        sql = "select rg.id as group_id, r.id, r.type, r.outputs, r.custom_module_id, r.custom_module_intent_id, r.position " \
              "from dialog_responsegroup as rg, dialog_response as r " \
              "where rg.intent_id=%s and rg.id=r.response_group_id order by rg.intent_id, r.response_group_id, r.position  "
        self.curs.execute(sql, (node_id, ))
        rows = self.curs.fetchall()

        return self.get_response_groups(rows)



    """
    Custom functions
    """

    def get_custom_intent_node_text(self, intent_id ):
        sql = "select text from custom_intentnode where id=%s "
        self.curs.execute(sql, (intent_id, ))
        row = self.curs.fetchone()
        if row is None:
            return None
        return row['text'].strip()

    def get_custom_intent_node_id_for_text(self, module_id, intent_text):
        sql = "select id from custom_intentnode where text=%s and module_id=%s"
        self.curs.execute(sql, (intent_text, module_id, ))
        row = self.curs.fetchone()
        if row is None:
            return None
        return int(row['id'])

    def get_custom_response_groups(self, node_id):
        sql = "select rg.id as group_id, r.id, r.type, r.outputs, r.custom_module_id, r.custom_module_intent_id, r.position " \
              "from custom_responsegroup as rg, custom_response as r " \
              "where rg.intent_id=%s and rg.id=r.response_group_id order by rg.intent_id, r.response_group_id, r.position "
        self.curs.execute(sql, (node_id, ))
        rows = self.curs.fetchall()

        return self.get_response_groups(rows)



    """
    Common functions
    """

    def get_custom_function(self, function_id):
        sql = "select * from custom_function where id=%s"
        self.curs.execute(sql, (function_id, ))
        row = self.curs.fetchone()
        return row

    def get_custom_function_for_module(self, module_id):
        sql = "select f.id, f.title, f.adapter, m.id as module_id, m.text as module_text from custom_function as f, wibo_module as m where f.id=m.custom_function_id and m.id=%s"
        self.curs.execute(sql, (module_id, ))
        row = self.curs.fetchone()
        return row

    def get_response_groups(self, rows):
        def get_outputs(type, outputs):
            items = []
            if type == 'media':
                sql = "select file_url from setting_media where id in ("+outputs.replace('|', ',')+")"
                self.curs.execute(sql, )
                rows = self.curs.fetchall()
                for row in rows:
                    items.append(row['file_url'])
            elif type == 'expression':
                sql = "select file_url from setting_expression where id in ("+outputs.replace('|', ',')+")"
                self.curs.execute(sql, )
                rows = self.curs.fetchall()
                for row in rows:
                    items.append(row['file_url'])
            elif type == 'command':
                sql = "select text from setting_command where id in ("+outputs.replace('|', ',')+")"
                self.curs.execute(sql, )
                rows = self.curs.fetchall()
                for row in rows:
                    items.append(row['text'])
            else:
                items = outputs.split('|')
            return items


        groups = []
        curr_group_id = -1
        for idx, row in enumerate(rows):

            print(row)
            if idx == 0:
                curr_group_id = row['group_id']
                group = {
                    'id': row['group_id'],
                    'data': []
                }
            if curr_group_id != row['group_id']:
                curr_group_id = row['group_id']
                groups.append(group)
                group = {
                    'id': row['group_id'],
                    'data': []
                }
            item = {
                'id': row['id'],
                'type': row['type'],
                'outputs': get_outputs(row['type'], row['outputs']),
                'custom_module_id': row['custom_module_id'],
                'custom_module_intent_id': row['custom_module_intent_id'],
                'position': row['position']
            }
            group['data'].append(item)

            if idx == len(rows) - 1:
                groups.append(group)


        return groups













    """
    Entity functions
    """

    def get_entities(self, chatbot_id):
        sql = "select id, text, data as dataset from setting_entity where chatbot_id=%s"
        self.curs.execute(sql, (chatbot_id, ))
        rows = self.curs.fetchall()
        return rows


    """
    Forbidden Word functions
    """
    def get_forbiddenwords(self, module_id):
        sql = "select * from settings_forbiddenwordintent where module_id=%s"
        self.curs.execute(sql, (module_id, ))
        rows = self.curs.fetchall()
        return rows


    """
    No Understanding functions
    """
    def get_nounderstandings(self, module_id):
        sql = "select * from settings_nounderstandingintent where module_id=%s"
        self.curs.execute(sql, (module_id, ))
        rows = self.curs.fetchall()
        return rows



    """
    conversation
    """
    def save_conversation(self, statement):
        sql = "insert into wibo_message(input, output, intent, channel, response_time, module_id, chatbot_id, user_key, created_date) " \
              "values (%s, %s, %s, %s, %s, %s, %s, %s, now());"

        if statement.request['user_key'] == -1 :
            statement.request['user_key'] = ''

        print(statement.serialize())

        self.curs.execute(sql, (
            statement.input['text'],
            statement.output['text'],
            statement.output['result']['intent'],
            statement.request['channel'],
            statement.output['result']['elapsed_time'],
            statement.output['result']['module_id'],
            statement.chatbot['id'],
            statement.request['user_key']
        ))
        self.conn.commit()

    """
    temp functions
    """
    def get_user_cid(self, user_key):

        if user_key == -1 or user_key == '' :
            return 1

        sql = "select id from user_ga_cid where tel=%s "
        self.curs.execute(sql, (user_key))
        rows = self.curs.fetchall()

        if rows is None or len(rows) == 0 :
            sql = "insert into user_ga_cid(tel) " \
                  "values (%s)"

            self.curs.execute(sql, (user_key))
            self.conn.commit()
            cid  = self.curs.lastrowid
        else :
            cid = rows[0]["id"]

        return cid

    """
    user life state
    """
    def get_user_life_state(self, user_key, state_keys):
        sql = "select * from user_life_state where updated_date >= cast(now() as date) and user_key=%s"

        if len(state_keys) > 0:
            sql += " and state_key in ("
            for state_key in state_keys:
                sql += "'" + state_key + "',"
            sql = sql[:-1] + ")"

        self.curs.execute(sql, (user_key))
        rows = self.curs.fetchall()

        state = {}
        for row in rows:
            state[row['state_key']] = row['state_value']

        return state


    def save_user_life_state(self, user_key, state_key, state_value):

        sql = "delete from user_life_state where updated_date >= cast(now() as date) and user_key=%s and state_key=%s"
        self.curs.execute(sql, (user_key, state_key))
        self.conn.commit()

        sql = "insert into user_life_state(user_key, state_key, state_value, updated_date) " \
              "values (%s, %s, %s, now());"
        self.curs.execute(sql, (user_key, state_key, state_value))
        self.conn.commit()



    """
    media file
    """
    def get_total_media_cnt(self, chatbot_id, music_class):
        sql = "select count(*) as cnt from setting_media where chatbot_id=%s and description=%s"
        self.curs.execute(sql, (chatbot_id, music_class, ))
        row = self.curs.fetchone()
        return row['cnt']

    def get_media_list(self, chatbot_id, media_ids, music_class):
        sql = "select * from setting_media where chatbot_id=%s and description=%s"

        if len(media_ids) > 0:
            sql += " and id not in ("
            for media_id in media_ids:
                sql += "'" + str(media_id) + "',"
            sql = sql[:-1] + ")"

        self.curs.execute(sql, (chatbot_id, music_class, ))
        rows = self.curs.fetchall()
        return rows




















    def get_maingraph(self, chatbot_id):
        collection = self.database.dialogflow_graph
        item = collection.find_one({"chatbot_id": int(chatbot_id), "type": "M"})
        return item


    def get_graph(self, graph_id):
        collection = self.database.dialogflow_graph
        item = collection.find_one({"graph_id": int(graph_id), "type": "S"})
        return item


    def has_chatbot(self, chatbot_id):
        collection = self.database.chatbots_chatbot
        item = collection.find_one({"id": int(chatbot_id)})
        if item is not None:
            return True
        return False

    def get_subgraph_mainnode(self, graph_id):
        collection = self.database.dialogflow_node
        item = collection.find_one({"graph_id": int(graph_id), "type": "R"})
        return item

    def get_nounderstanding_output(self, chatbot_id, logic_id):
        module = self.database.pipeline_module.find_one({"chatbot_id": int(chatbot_id), 'type': 'N', 'id': logic_id})
        return module['output']

    """
    intent functions
    """

    def get_intent(self, intent_title):
        intent = self.database.management_intent.find_one({"title": intent_title})
        return intent


    """
    function functions
    """

    def get_function(self, function_id):
        function = self.database.management_function.find_one({"id": int(function_id)})
        return function

    """
    database 리소스를 구함 , conn, curs
    """
    def get_resource(self):
        return self.conn, self.curs