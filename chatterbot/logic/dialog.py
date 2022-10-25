from chatterbot.logic.logic_adapter import LogicAdapter
from chatterbot.functions import recognize_intent, make_response
# from chatterbot.comparisons import cosine_similarity_check
from operator import itemgetter

import json
import requests

class DialogAdapter(LogicAdapter):

    def can_process(self, statement):
        return True


    def process(self, input_statement):
        return self.get_response(input_statement)


    def get_response(self, statement):

        DICT_PATH = "chatterbot/logic/dialog/"
        dict_logic_intent = json.load(open(DICT_PATH + "dialog_intent_adapter.json"))

        intent_nodes = self.chatbot.storage.get_dlg_intent_nodes(self.id)
        response_node = self.intent_process(intent_nodes, statement)

        response_groups = self.chatbot.storage.get_dlg_response_groups(response_node['node_id'])
        response_groups = self.response_node_check(response_groups)
        
        response_group = self.select_response(response_list=response_groups)

        statement.set_result(module=self.title, 
                             intent=response_node['node_text'], 
                             confidence=response_node['confidence'],
                             chatbot_id=int(self.chatbot_id),
                             logic_property='dialogue_logic'
                            )

        statement.request['user_key'] = self.chatbot.user_key

        for response in response_group['data']:
            statement = make_response(response, statement)

        output_text = statement.output[0]['text']

        if output_text in dict_logic_intent.keys():
            statement = self.logic_adapter(dict_logic_intent[output_text], statement)

        print("output_text: ", statement.output[0]['text'])

        return statement


    def response_node_check(self, response_groups):
        if len(response_groups) > 1:
            for response in response_groups:
                outputs_text = response.get('data', [])[0]['outputs']
                if outputs_text:
                    return [response]

        else:            
            return response_groups


    def intent_process(self, intent_nodes, statement):
        
        max_index = 5
        limit_confidence = 40

        node_list = []
        for intent_node in intent_nodes:
            if recognize_intent(intent_node, statement):
                node_list.append(intent_node)

        if len(node_list) == 0:
            response_node = {
                    'node_id': int(10518),
                    'node_text': '무응답',
                    'confidence': 0.0
            }

            return response_node

        else: 
            if len(node_list) >= max_index:
                node_sort = sorted(node_list, key=itemgetter('confidence'), reverse=True)

                return self.flask_response_node(self.intent_dict_gen(statement.input['text'], limit_confidence, node_sort[:max_index]), limit_confidence)

            else:
                node_sort = sorted(node_list, key=itemgetter('confidence'), reverse=True)

                return self.flask_response_node(self.intent_dict_gen(statement.input['text'], limit_confidence, node_sort), limit_confidence)


    def intent_dict_gen(self, input, limit_confidence, node_sort):
        return {
            "input_text":input,
            "limit_confidence":limit_confidence,
            "data":node_sort
        }


    def flask_response_node(self, intent_dict, limit_confidence):
        # URL = 'http://0.0.0.0:10733/api/response'
        # URL = 'http://0.0.0.0:5003/api/response'
        # URL = 'http://13.125.34.74:10733/api/response'
        URL = 'http://34.64.190.233:10733/api/response'
        headers = {'Content-Type': 'application/json; charset=utf-8'}

        try:
            res = requests.post(URL, data=json.dumps(intent_dict), headers=headers)
            data_fin = res.json()

            if data_fin['cosine_similarity'] >= limit_confidence:
                response_node = {
                    'node_id': int(data_fin['id']),
                    'node_text': data_fin['text'],
                    'confidence': data_fin['cosine_similarity']
                }

            else :
                response_node = {
                    'node_id': int(10518),
                    'node_text': '무응답',
                    'confidence': data_fin['cosine_similarity']
                }

        except:
            print('Google instance error')
            response_node = {
                'node_id': int(10518),
                'node_text': '무응답',
                'confidence': 0.0
            }
            
        return response_node


    def logic_adapter(self, adapter_name, statement):

        if self.chatbot.function_match[adapter_name].can_process(statement):
            statement = self.chatbot.function_match[adapter_name].process(statement)
            
        return statement