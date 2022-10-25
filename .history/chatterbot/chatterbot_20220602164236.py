import logging
from chatterbot.storage import StorageAdapter
from chatterbot.logic import LogicAdapter
from chatterbot.input import InputAdapter
from chatterbot.output import OutputAdapter
from chatterbot.storage.rediscache import RedisCache
import utils.ga_helper as ga_helper

from chatterbot import utils


class ChatBot(object):
    """
    A conversational dialog chat bot.
    """
    def __init__(self, chatbot_id, **kwargs):

        # setting class properties
        # self.chatbot_id = kwargs.get('chatbot_id', None)
        self.chatbot_id = chatbot_id

        # initializing storage adapter
        storage_adapter = kwargs.get('storage_adapter', 'chatterbot.storage.MariaDatabaseAdapter')
        utils.validate_adapter_class(storage_adapter, StorageAdapter)
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
        self.logic_adapters = []

        def set_logic_adapter(id, title='', adapter=''):
            utils.validate_adapter_class(adapter, LogicAdapter)
            logic_adapter = utils.initialize_class(adapter, self, **kwargs)
            logic_adapter.id = id
            logic_adapter.title = title
            self.logic_adapters.append(logic_adapter)

        modules = self.storage.get_modules(self.chatbot_id)

        for module in modules:
            if module['type'] == 'DF':
                set_logic_adapter(module['id'], title=module['text'], adapter='chatterbot.logic.DialogflowAdapter')
            elif module['type'] == 'DI':
                set_logic_adapter(module['id'], title=module['text'], adapter='chatterbot.logic.DialogAdapter')
            elif module['type'] == 'CU':
                custom_function = self.storage.get_custom_function(module['custom_function_id'])    #날씨, 날짜, 시간 ETC..
                set_logic_adapter(module['id'], title=module['text'], adapter='chatterbot.logic.'+custom_function['adapter'])

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

        # initializing etc properties
        self.enabled_confidence_threshold = True
        self.confidence_threshold = 0.1
        self.logger = logging.getLogger(__name__)

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

        # user_key = output_statement.request['user_key']
        # self.cache_storage.save_intent(user_key, output_statement.output['result']['intent'])
        # self.storage.save_conversation(output_statement)

        return output_statement.serialize()


    def generate_response(self, input_statement):
        # results = []
        result = None

        for adapter in self.logic_adapters:

            self.logger.info(
                'Adapter: {}'.format(adapter.class_name)
            )

            if adapter.can_process(input_statement):
                # adapter.confidence_threshold = self.confidence_threshold

                statement = adapter.process(input_statement)
                if statement is None:
                    continue

                # results.append((statement.get_output_confidence(), statement,))

                # 특정 confidence_threshold 보다 높으면 답변으로 선정
                get_confidence = statement.get_output_confidence()
                check_confidence = self.confidence_threshold
                
                # if get_confidence >= check_confidence:
                if statement.get_output_confidence() >= self.confidence_threshold:
                # if statement.get_output_confidence():
                    result = statement
                    # result.set_output_module(adapter.id, adapter.title)
                    break

            else:
                self.logger.info(
                    'Not processing the statement using {}'.format(adapter.class_name)
                )

        # 만족된 결과가 없을 때..
        if result is None:
            from .conversation import Statement
            result = Statement(self)

        return result


    class ChatBotException(Exception):
        pass
