from chatterbot.logic import LogicAdapter
from chatterbot import response_selection
from chatterbot.utils import replace_entity


from chatterbot.functions import recognize_intent, make_response
from communication import post


class DialogAdapter(LogicAdapter):

    def can_process(self, statement):
        return True


    def process(self, input_statement):
        return self.get_response(input_statement)


    def get_response(self, statement):

        response_node = None

        intent_nodes = self.chatbot.storage.get_dlg_intent_nodes(self.id)
        
        intent_list = []
        intent_id = []  
        for intent_node in intent_nodes:
            if recognize_intent(intent_node, statement):
                
                intent_list.append(intent_node['text'])
                intent_id.append(intent_node['id'])
            
        # response_node = post(intent_list, intent_id, statement.input['text'])
        
        print(intent_list)
        print(intent_id)

       
        # 응답 셋팅
        # if response_node is not None:
        try :
            
            response_node = post(intent_list, intent_id, statement.input['text'])
            
            response_groups = self.chatbot.storage.get_dlg_response_groups(response_node['node_id'])
            response_group = self.select_response(response_list=response_groups)

            statement.set_result(module=self.title, 
                                 intent=response_node['node_text'], 
                                 confidence=100 * round(response_node["confidence"], 4)
                                )
            for response in response_group['data']:
                statement = make_response(response, statement)

            print('dialog', statement.result)
 
        except:
            
            confidence_list = []       
            for text in intent_list:
                from chatterbot.comparisons import levenshtein_distance
                import numpy as np
                confidence = levenshtein_distance(statement.input['text'], text)
                confidence_list.append(confidence)
            
            print(confidence_list)
            
            response_node = {
                'node_id': intent_id[np.argmax(confidence_list)],
                'node_text': intent_list[np.argmax(confidence_list)],
                'confidence': 1.0
            }

            response_groups = self.chatbot.storage.get_dlg_response_groups(response_node['node_id'])
            response_group = self.select_response(response_list=response_groups)

            statement.set_result(module=self.title, 
                                 intent=response_node['node_text'], 
                                 confidence=1.0
                                )
            for response in response_group['data']:
                statement = make_response(response, statement)
                
            print('dialog', statement.result)

        return statement





