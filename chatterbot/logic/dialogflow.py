from chatterbot.logic import LogicAdapter
from chatterbot import response_selection
from chatterbot.utils import replace_entity

from chatterbot import utils

from chatterbot.functions import recognize_intent, make_response



class DialogflowAdapter(LogicAdapter):
    """
    A logic adapter that returns a response based on known responses to
    the closest matches to the input statement.
    """

    def can_process(self, statement):
        """
        Check that the chatbot's storage adapter is available to the logic
        adapter and there is at least one statement in the database.
        """
        return True
        # return self.chatbot.storage.has_chatbot(statement.chatbot_id)

    def process(self, input_statement):
        return self.get_chat_response(input_statement)


    def get_chat_response(self, statement):

        response_node = None

        # 현재 진행중인 노드 의도 분석
        if 'dialogflow' in statement.context:
            statement.context['dialogflow']['visit_count'] += 1
            start_node = self.chatbot.storage.get_dlgf_node_for_graph(statement.context['dialogflow']['graph_id'],  statement.context['dialogflow']['node_id'])

            # GET 다음 노드
            next_nodes = self.chatbot.storage.get_dlgf_next_nodes(start_node['node_key'])

            # 다음 노드가 없고 현재 루트노드가 아니라면 초기화
            if len(next_nodes) == 0 and start_node['node_type'] != 'R':
                del statement.context['dialogflow']
            else:
                for next_node in next_nodes:
                    if recognize_intent(next_node, statement):
                        response_node = {
                            'graph_id': start_node['graph_id'],
                            'node_id': next_node['id'],
                            'node_key': next_node['key'],
                            'node_text': next_node['text'],
                            'confidence': 1.0,
                            'condition': 'default'
                        }
                        statement.context['dialogflow'] = {
                            'graph_id': response_node['graph_id'],
                            'node_id': response_node['node_id'],
                            'visit_count': 0
                        }
                        break

                if response_node is None: # 재방문일때!!!

                    def get_response_condition(max_visit_count, visit_count):
                        condition = None
                        if visit_count == max_visit_count:
                            if self.chatbot.storage.has_dlgf_last_visit_response(start_node['node_id']):
                                condition = 'last_visit'
                        elif visit_count < max_visit_count:
                            if self.chatbot.storage.has_dlgf_re_visit_response(start_node['node_id']):
                                condition = 're_visit'
                        return condition

                    condition = get_response_condition(start_node['node_max_visit_count'], statement.context['dialogflow']['visit_count'])

                    if condition is not None:
                        response_node = {
                            'graph_id': start_node['graph_id'],
                            'node_id': start_node['node_id'],
                            'node_key': start_node['node_key'],
                            'node_text': start_node['node_text'],
                            'confidence': 0.0,
                            'condition': condition
                        }
                        statement.context['dialogflow'] = {
                            'graph_id': response_node['graph_id'],
                            'node_id': response_node['node_id'],
                            'visit_count': statement.context['dialogflow']['visit_count']
                        }

        # 모든 그래프 루트 노드 의도 분석
        if response_node is None:
            start_nodes = self.chatbot.storage.get_dlgf_root_nodes_for_module(self.id)

            # Find the closest matching Intent
            for start_node in start_nodes:

                # GET 다음 노드
                next_nodes = self.chatbot.storage.get_dlgf_next_nodes(start_node['node_key'])

                for next_node in next_nodes:
                    if recognize_intent(next_node, statement):
                        response_node = {
                            'graph_id': start_node['graph_id'],
                            'node_id': next_node['id'],
                            'node_key': next_node['key'],
                            'node_text': next_node['text'],
                            'confidence': 1.0,
                            'condition': 'default'
                        }
                        statement.context['dialogflow'] = {
                            'graph_id': response_node['graph_id'],
                            'node_id': response_node['node_id'],
                            'visit_count': 0
                        }
                        break

                if response_node is not None:
                    break

        # 응답 셋팅
        if response_node is not None:

            response_groups = self.chatbot.storage.get_dlgf_response_groups(response_node['node_id'], response_node['condition'])
            response_group = self.select_response(response_list=response_groups)

            for response in response_group['data']:
                statement = make_response(response, statement)

            # 마지막 방문이거나 다음 노드 없으면 초기화
            if response_node['condition'] == 'last_visit' or self.chatbot.storage.get_dlgf_next_nodes_cnt(response_node['node_key']) == 0:
                del statement.context['dialogflow']

            statement.result['module'].insert(0, self.title)
            statement.result['intent'].insert(0, response_node['node_text'])
            statement.result['confidence'] = 1.0

        return statement




