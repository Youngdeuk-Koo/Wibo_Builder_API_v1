
import pandas as pd
from collections import defaultdict

class ResponseSet() :
    def __init__(self, intent, response, keywords, title, category_id):
        self.intents = intent
        self.response = response
        self.keywords = keywords
        self.title = title
        self.category_id = category_id

    def max_len(self):
        if self.keywords is None or len(self.keywords) == 0 :
            return 0
        max = 0
        for keyword in self.keywords :
            if len(keyword) > max :
                max = len(keyword)

        return max


class ResponseUtil() :

    def __init__(self, chat_id, faqDataDB):
        self.intent_response = defaultdict(list)
        self.faqDataDB = faqDataDB
        self.entity_keyword = self.faqDataDB.entity_keywords(chat_id)
        #self.intent_index, self.intent_text = faqDataDB.intents(12)

    def make_response_set(self, intent_rules):
        if intent_rules is None :
            return []

        results = []
        for keyword, response, intent_id, title, category_id, intent_ids in intent_rules :
            responseSet = ResponseSet(intent_ids, response, keyword, title, category_id)
            results.append(responseSet)

        return results


    def check_response(self, module_id, intents, question):
        # print("intents ===>", intents)

        intent_indexs = []

        for intent in intents :
            intent_indexs.append(str(intent))

        intent_rules = self.faqDataDB.intent_rules(module_id, intent_indexs)
        responseSets = self.make_response_set(intent_rules)

        if len(responseSets) == 0 :
            return None, None, None

        results = []
        for responseSet in responseSets :
            is_check, collect_cnt= self.check_rule_sentences(question, responseSet)

            if is_check :
                results.append((responseSet, collect_cnt))

        if len(results) == 0 :
            return None, None, None

        results = sorted(results, key=lambda x: x[1], reverse=True)

        max_cnt = results[0][1]

        responses = []
        for result in results :
            if result[1] == max_cnt :
                responses.append(result)
            else :
                break
        selResponseSet = None

        if len(responses) == 1 :
            selResponseSet = responses[0][0]
            #return responses[0][0].response, responses[0][0].title
        else :
            for response in responses :
                responseSet = response[0]
                if selResponseSet is None :
                    selResponseSet = responseSet
                else :
                    if selResponseSet.max_len() < responseSet.max_len() :
                        selResponseSet = responseSet

        category = self.faqDataDB.category(selResponseSet.category_id)

        category_name = ''

        if category is not None :
            category_name = category['title']

        return selResponseSet.response, selResponseSet.title, category_name


    def check_rule_sentences(self, question, responseSet):


        collect_cnt = 0
        rule_keywords = responseSet.keywords
        question = question.replace(" ", "")
        question = question.lower()

        #print(responseSet.title, " of intents : ", responseSet.intents)

        if (rule_keywords is None or len(rule_keywords) == 0) and  48 not in responseSet.intents:
            return True, 0

        #print("====> check out: ", question, rule_keywords)
        for keyword in rule_keywords:

            if len(keyword) == 0 :
                continue

            if keyword[0] == '@':
                keyword = keyword[1:].strip()

                if keyword not in self.entity_keyword : continue

                word_list = self.entity_keyword[keyword]
                # print("====>", word_list)
                is_keyword = False
                for word in word_list:
                    if word in question:
                        is_keyword = True
                        collect_cnt += 1
                        break

                #print(" ### >", is_keyword)
                if not is_keyword:
                    return False, 0

            else:
                if keyword in question:
                    collect_cnt += 1
                    continue

       # print("middle ---> ", rule_keywords, collect_cnt, rule_keywords)
        if collect_cnt == 0 and '48' in responseSet.intents :
            return False, 0
       # print("middle 2---> ", rule_keywords, collect_cnt, len(rule_keywords))
        if rule_keywords is not None and len(rule_keywords) > 0 and  len(rule_keywords)  != collect_cnt:
            return False, 0

        # print("rule =====>", rule_keywords, collect_cnt)
        return True, collect_cnt