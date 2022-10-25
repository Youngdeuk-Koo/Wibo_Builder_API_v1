import random

class RandomResponseUtil() :

    def __init__(self, cache):
        self.cache = cache


    def get_response(self, user_key, module_id, intent, response):

        key = user_key + "_" + str(module_id) + "_" + intent


        answer = self.cache.rpop(key)
        if answer is None:
            random.shuffle(response)
            answer = response.pop()
            self.cache.lpush(key, *response)

        return answer