from chatterbot.logic.logic_adapter import LogicAdapter
from chatterbot.functions import recognize_intent, make_response
from chatterbot.comparisons import cosine_similarity_check

from chatterbot import utils
import settings
import numpy as np
import json


class DialogAdapter(LogicAdapter):

    def can_process(self, statement):
        return True


    def process(self, input_statement):
        return self.get_response(input_statement)


    def get_response(self, statement):

        DICT_PATH = "chatterbot/logic/dialog/"
        dict_logic_intent = json.load(open(DICT_PATH + "dialog_intent_adapter.json"))

        response_node = None


        intent_nodes = self.chatbot.storage.get_dlg_intent_nodes(self.id)
        response_node = self.intent_process(intent_nodes, statement)

        response_groups = self.chatbot.storage.get_dlg_response_groups(response_node['node_id'])
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
    def intent_process(self, intent_nodes, statement):
        
        max_index = 5

        intent = {round(intent_node['confidence'], 1) : {'intent_id':intent_node['id'], 'intent_text':intent_node['text']} for intent_node in intent_nodes if recognize_intent(intent_node, statement)}
        input_embedding_text = self.model.encode(statement.input['text'])
        

        if len(intent) == 0:
            response_node = {
                    'node_id': int(700),
                    'node_text': '무응답',
                    'confidence': 0.0
            }
            return response_node


        elif len(intent) > max_index:
            sorted_intent = sorted(intent.items(), key = lambda item: item[0], reverse = True)[:max_index]

            score = []
            for info in sorted_intent:
                db_embedding_text = self.model.encode(info[1]['intent_text'])
                confidence = round(cosine_similarity_check(input_embedding_text, db_embedding_text).tolist(), 2) * 100
                info[1]['cosine_similarity'] = confidence
                score.append(confidence)

            max_confidenc_index = np.argmax(score).tolist()
            max_intent = sorted_intent[max_confidenc_index]


        else:
            sorted_intent = sorted(intent.items(), key = lambda item: item[0], reverse = True)

            score = []
            for info in sorted_intent:
                db_embedding_text = self.model.encode(info[1]['intent_text'])
                confidence = round(cosine_similarity_check(input_embedding_text, db_embedding_text).tolist(), 2) * 100
                info[1]['cosine_similarity'] = confidence
                score.append(confidence)

            max_confidenc_index = np.argmax(score).tolist()
            max_intent = sorted_intent[max_confidenc_index]


        if max_intent[1]['cosine_similarity'] >= 25 :
            response_node = {
                'node_id': int(max_intent[1]['intent_id']),
                'node_text': max_intent[1]['intent_text'],
                'confidence': max_intent[1]['cosine_similarity']
            }

        else :
            response_node = {
                    'node_id': int(700),
                    'node_text': '무응답',
                    'confidence': max_intent[1]['cosine_similarity']
            }

        
        print("input_text: ", statement.input['text'])
        # print("confidence_list: ", intent_confidence)            
        # print("intent_list: ", intent_text)
        # print("intent_id: ", intent_id)
        print("response_node: ", response_node)
        # print("score: ", score)

        return response_node

    def logic_adapter(self, adapter_name, statement):

        if self.chatbot.function_match[adapter_name].can_process(statement):
            statement = self.chatbot.function_match[adapter_name].process(statement)

        # else:
        #     self.logging.war(
        #         'Failed to load adapter'
        #     )
            
        return statement