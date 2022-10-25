
from chatterbot.storage import StorageAdapter
from chatterbot.logic import LogicAdapter
from chatterbot.input import InputAdapter
from chatterbot.output import OutputAdapter
from chatterbot.storage.rediscache import RedisCache
from chatterbot import utils
from collections import defaultdict
import datetime as dt
import logging

cnt = 0

class ChatBot(object):
    
    """
    A conversational dialog chat bot.
    """
    def __init__(self, chatbot_id, user_key, **kwargs):   
        
        self.chatbot_id = chatbot_id
        self.user_key = user_key
        self.logging = logging 
        ##########################
        self.total_count = 0
        self.user_count = defaultdict(int, {0:0})
        ##########################
        # self.created_at = datetime.now()                                                                 # 5. chatbot_id를 self 인스턴스로 포함

        # initializing storage adapter
        storage_adapter = kwargs.get('storage_adapter', 'chatterbot.storage.MariaDatabaseAdapter')      # 6. kwargs(user_key, setting)로 전달 받은 Dict형태의 Key와 Value를 추출
        utils.validate_adapter_class(storage_adapter, StorageAdapter)                                   # 7. Class의 상속 여부 확인을 검사 한다(변수값: kwarg에 담겨 있던 어댑터 명과 경로, 실제 Class)
        self.storage = utils.initialize_class(storage_adapter, **kwargs)
        self.cache_storage = RedisCache()

        # initializing input adapter
        input_adapter = kwargs.get('input_adapter', 'chatterbot.input.APIAdapter')
        utils.validate_adapter_class(input_adapter, InputAdapter)
        self.input = utils.initialize_class(input_adapter, self, **kwargs)

        # initializing output adapter
        output_adapter = kwargs.get('output_adapter', 'chatterbot.output.APIAdapter')
        utils.validate_adapter_class(output_adapter, OutputAdapter)
        self.output = utils.initialize_class(output_adapter, self, **kwargs)

        # initializing logic adapters
        self.function_match = {}



        def set_logic_adapter(id, title='', adapter='', name=''):
            utils.validate_adapter_class(adapter, LogicAdapter)
            logic_adapter = utils.initialize_class(adapter, self, **kwargs)
            logic_adapter.id = id
            logic_adapter.title = title

            self.function_match[name] = logic_adapter


        def dia_logic_adapter(id, title='', adapter=''):
            utils.validate_adapter_class(adapter, LogicAdapter)
            dia_adapter = utils.initialize_class(adapter, self, **kwargs)
            dia_adapter.id = id
            dia_adapter.title = title
            return dia_adapter

        modules = self.storage.get_modules(self.chatbot_id)

        for module in modules:

            if module['type'] == 'CU':
                custom_function = self.storage.get_custom_function(module['custom_function_id'])    #날씨, 날짜, 시간 ETC..
                set_logic_adapter(module['id'], title=module['text'], adapter='chatterbot.logic.'+custom_function['adapter'], name=custom_function['adapter'])

            elif module['type'] == 'DI':
                self.dia_adapter = dia_logic_adapter(module['id'], title=module['text'], adapter='chatterbot.logic.DialogAdapter')

        # initializing preprocessors
        preprocessors = kwargs.get(
            'preprocessors', [
                # 'chatterbot.preprocessors.recognize_entity',
                'chatterbot.preprocessors.pos_tagging',
                'chatterbot.preprocessors.remove_blank'
            ]
        )
        self.preprocessors = []
        for preprocessor in preprocessors:
            self.preprocessors.append(utils.import_module(preprocessor))


    def __call__(self, user_key):
        self.total_count += 1
        self.user_count[user_key] += 1
        print(self.total_count)
        print(self.user_count)

        return 0

    # GET으로 받을때 리스폰값 생성
    def get_init_response(self):
        statement = self.input.process_input({})
        statement = self.output.process_response(statement)
        return statement.serialize()


    def get_response(self, statement=None, **kwargs):

        if statement is None:
            raise self.ChatBotException(
                'argument is required. Neither was provided.'
            )

        if isinstance(statement, dict):
            statement.update(kwargs)
            kwargs = statement

        input_statement = self.input.process_input(kwargs)
        for preprocessor in self.preprocessors:
            input_statement = preprocessor(input_statement)

        output_statement = self.generate_response(input_statement)
        output_statement = self.output.process_response(output_statement)

        utils.log_write('nlp', output_statement)

        return output_statement.serialize()


    def generate_response(self, input_statement):
        result = None

        if self.dia_adapter.can_process(input_statement):
            statement = self.dia_adapter.process(input_statement)
            result = statement

        # else:
        #     self.logging.war(
        #         'Failed to load adapter'
        #     )

        # 만족된 결과가 없을 때..
        if result is None:
            from .conversation import Statement
            result = Statement(self)

        return result


    # def log_write(self, statement):
    #     import time
    #     global cnt
    #     cnt += 1

    #     statement.context['visit_count'] = cnt
        
    #     n = time.localtime().tm_wday

    #     days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    #     with open('./log/nlp_log/' + 'nlp_' + str(dt.datetime.now().strftime("%Y_%m_%d")) + '_' + str(days[n]) +'.txt', 'a+') as f:
    #         f.write(dt.datetime.now().strftime("%Y-%m-%d" + "    " + "%H:%M:%S") + "    " +
    #         str(cnt) + "    " + 
    #         str(self.user_key) + "    " + 
    #         str(statement.input['text']) + "    " + 
    #         str(statement.output[0]['text']) +  "    " + 
    #         str(statement.result['intent']) +  "    " + 
    #         str(statement.result['confidence']) + '\n')


    class ChatBotException(Exception):
        pass
