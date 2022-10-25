from chatterbot.logic import LogicAdapter
from chatterbot import response_selection
from chatterbot.utils import replace_entity

# from chatterbot.functions import recognize_intent, make_response
from chatterbot.functions_copy import recognize_intent, make_response
from chatterbot.comparisons_copy import cosine_similarity_check
import json
import torch
import numpy as np

device = torch.device("cpu")
model = torch.load("SAVE_MODEL_DIR/model", map_location=device)

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
                # response_node = {
                #     'node_id': intent_node['id'],
                #     'node_text': intent_node['text'],
                #     'confidence': 1.0
                # }
                # break

                
                intent_list.append(intent_node['text'])
                intent_id.append(intent_node['id'])

        print(intent_list)
        intent_list_copy = intent_list
        intent_embedding = model.encode(intent_list_copy)
        
        import time
        start = time.time()
        
        score = []
        for embedding in intent_embedding:
            statement_input_embedding = model.encode(statement.input['text'])
            similarity = cosine_similarity_check(statement_input_embedding, embedding)
            score.append(similarity)
            
        result = score[np.argmax(score)].tolist()
        # index_check = np.argmax(score)
        print(result)    
        end = time.time()
        pre = end -start
        
        if result >= 0.45 :
            response_node = {
                    'node_id': intent_id[np.argmax(score)],
                    'node_text': intent_list[np.argmax(score)],
                    'confidence': result
            }       
            
        else :
            response_node = {
                    'node_id': 700,
                    'node_text': '무응답',
                    'confidence': result
            }
            
        
        # 응답 셋팅
        if response_node is not None:

            response_groups = self.chatbot.storage.get_dlg_response_groups(response_node['node_id'])
            response_group = self.select_response(response_list=response_groups)

            statement.set_result(module=self.title, intent=response_node['node_text'], confidence=1.0)
            for response in response_group['data']:
                statement = make_response(response, statement)

            print('dialog', statement.result)

        return statement





