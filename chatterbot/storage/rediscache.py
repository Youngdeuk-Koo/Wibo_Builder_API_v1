import redis
import random

class RedisCache():

    def __init__(self):
        host_name = '127.0.0.1'
        self.r = redis.StrictRedis(host=host_name, charset="utf-8", decode_responses=True, port=6379, password="7890uiop")

    @property
    def storage(self):
        return self.r


    def random_cache_response(self, key, outputs):
        import random

        if len(outputs) == 1:
            return outputs[0]

        answer = self.r.rpop(key)
        if answer is None:
            random.shuffle(outputs)
            answer = outputs.pop()
            self.r.lpush(key, *outputs)

        return answer
