from chatterbot.adapters import Adapter
from chatterbot.utils import import_module
from chatterbot.logic.util.response_utils import RandomResponseUtil

class LogicAdapter(Adapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        from chatterbot.comparisons import levenshtein_distance
        from chatterbot.response_selection import get_random_response
             
        self.chatbot_id = self.chatbot.chatbot_id
        self.user_key = self.chatbot.user_key

        # Import string module parameters
        if 'statement_comparison_function' in kwargs:
            import_path = kwargs.get('statement_comparison_function')
            if isinstance(import_path, str):
                kwargs['statement_comparison_function'] = import_module(import_path)

        if 'response_selection_method' in kwargs:
            import_path = kwargs.get('response_selection_method')
            if isinstance(import_path, str):
                kwargs['response_selection_method'] = import_module(import_path)


        self.confidence_threshold = kwargs.get(
            'confidence_threshold', 0.8
        )

        self.maximum_similarity_threshold = kwargs.get(
            'maximum_similarity_threshold', 0.8
        )

        self.excluded_words = kwargs.get('excluded_words')

        self.search_page_size = kwargs.get(
            'search_page_size', 1000
        )

        # By default, compare statements using Levenshtein distance
        self.compare_statements = kwargs.get(
            'statement_comparison_function',
            levenshtein_distance
        )

        # By default, select the first available response
        self.select_response = kwargs.get(
            'response_selection_method',
            get_random_response
        )

        self.randomResponseUtil = RandomResponseUtil(self.chatbot.cache_storage.storage)
        


    def can_process(self, statement):
        return True

    def process(self, statement):
        raise self.AdapterMethodNotImplementedError()

    @property
    def class_name(self):
        return str(self.__class__.__name__)

