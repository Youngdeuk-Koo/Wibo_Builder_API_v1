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
        
        intent_list, intent_id = [], []
        for intent_node in intent_nodes:
            if recognize_intent(intent_node, statement):    
                intent_list.append(intent_node['text'])
                intent_id.append(intent_node['id']) 
        
        print(intent_list)
        print(intent_id)

        # 코사인 시밀리터리 적용
        try :
            
            response_node = post(intent_list, intent_id, statement.input['text'])  
            
            response_groups = self.chatbot.storage.get_dlg_response_groups(response_node['node_id'])
            response_group = self.select_response(response_list=response_groups)

            statement.set_result(module=self.title, 
                                 intent=response_node['node_text'], 
                                 confidence=100 * response_node['confidence'],
                                 confidence_type="cosine_similarity"
                                )
            
            for response in response_group['data']:
                statement = make_response(response, statement)

            print('dialog', statement.result)
        
        # 코사인 시밀리터리 꺼져 있을 경우 대체    
        except:
            
            from chatterbot.comparisons import levenshtein_distance
            import numpy as np
            
            confidence_list = []
            for text in intent_list:                
                confidence_list.append(levenshtein_distance(statement.input['text'], text))
                
            self.confidence = 100 * confidence_list[np.argmax(confidence_list)]
            
            if self.confidence >= 60: 
                response_node = {
                    'node_id': intent_id[np.argmax(confidence_list)],
                    'node_text': intent_list[np.argmax(confidence_list)],
                    'confidence': self.confidence
                }  
            
            else:      
                response_node = {
                    'node_id': 700,
                    'node_text': '무응답',
                    'confidence': self.confidence
                }       
            
            response_groups = self.chatbot.storage.get_dlg_response_groups(response_node['node_id'])
            response_group = self.select_response(response_list=response_groups)

            statement.set_result(module=self.title, 
                                 intent=response_node['node_text'], 
                                 confidence=response_node['confidence'],
                                 confidence_type="levenshtein_distance"
                                )
            
            for response in response_group['data']:
                statement = make_response(response, statement)

        return statement





