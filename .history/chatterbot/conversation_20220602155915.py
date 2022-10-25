from datetime import datetime

class Statement():


    def __init__(self, chatbot, **kwargs):

        self.chatbot = chatbot
        self.storage = chatbot.storage
        self.cache_storage = chatbot.cache_storage

        #
        # self.chatbot = {
        #     'id': chatbot.chatbot_id
        # }
        #

        self.request = kwargs.get('request', {
            'user_key': '',
            'channel': '',
            'remote_addr': '',
        })

        self.context = kwargs.get('context', {
            'variables': {},
            'visit_count': 0,
            'created_at': self.get_datetime_now_str()
        })

        self.input = kwargs.get('input', {
            'text': None
        })

        self.output = []

        self.result = {
            'module': [],
            'intent': [],
            'confidence': 0.0,
            'confidence_property': '',
            'elapsed_time': 0            
        }

        self.created_at = datetime.now()


    def init_context(self):
        self.context = {
            'variables': {},
            'visit_count': 0,
            'created_at': self.get_datetime_now_str()
        }

    def serialize(self):
        output = []
        for item in self.output:
            if 'text' in item:
                item['type'] = 'text'
                item['data'] = item['text']
                output.append(item)
            elif 'expression' in item:
                item['type'] = 'expression'
                item['data'] = item['expression']
                output.append(item)
            elif 'media' in item:
                item['type'] = 'media'
                item['data'] = item['media']
                output.append(item)
            elif 'command' in item:
                item['type'] = 'command'
                item['data'] = item['command']
                output.append(item)

        return {
            'request': self.request,
            'context': self.context,
            'input': self.input,
            'output': output,
            'result': self.result,
        }


    def set_result(self, module, intent, confidence, confidence_type):
        self.result['module'].append(str(module))
        self.result['intent'].append(str(intent))
        self.result['confidence'] = confidence + 0.1
        self.result['confidence_property'] = confidence_type
        


    def set_elapsed_time(self):
        end = datetime.now()
        elapsed = end - self.created_at
        self.result['elapsed_time'] = elapsed.microseconds/1000


    def get_output_confidence(self):
        return self.result['confidence']


    def is_timeover(self):
        pre = datetime.strptime(self.context['created_at'], "%m/%d/%Y, %H:%M:%S")
        now = datetime.now()
        delta = now - pre
        if delta.seconds > 100:
            return True
        return False


    def get_cache_key(self):
        chatbot = self.chatbot.chatbot_id
        print('chatbot : {}'.format(chatbot))
        user = self.request.get('user_key', '')
        module = ''.join(self.result['module'])
        intent = ''.join(self.result['intent'])
        return str(chatbot)+str(user)+str(module)+str(intent)












    def is_init(self):
        if self.output['result']['module_id'] == -1:
            return True
        return False

    def get_datetime_now_str(self):
        now = datetime.now()
        return now.strftime("%m/%d/%Y, %H:%M:%S")


    def get_chatbot_id(self):
        return self.chatbot.chatbot_id
        # return self.chatbot['id']



    def set_output(self, _text, _module, _intent, _confidence):
        self.output['text'] = _text
        # self.output['result']['module'] = _module
        self.output['result']['intent'] = _intent
        self.output['result']['confidence'] = _confidence

    def set_output_module(self, _id, _title):
        self.output['result']['module_id'] = _id
        self.output['result']['module_title'] = _title

    def set_output_cmd(self, _cmd):
        self.output['cmd'] = _cmd

    def set_output_url(self, _url):
        self.output['url'] = _url

