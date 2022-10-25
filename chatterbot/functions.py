import numpy as np
import re

def recognize_intent(next_node, statement):
    match_functions = {
        'sentence': match_sentence,
        'keyword': match_keyword,
        'corpus': match_corpus,
        'pos': match_pos
    }
    for group in next_node.get('data', []):
        arr_logic = group.get('data', [])
        is_matched = True if len(arr_logic) > 0 else False
        for logic in arr_logic:
            if not match_functions[logic['type']](logic, statement):
                is_matched = False
                break
        if is_matched:
            next_node['confidence'] = statement.confidence
            del(next_node['data'])
            return True
    return False


def match_sentence(logic, statement):
    def max_confidence(confidence_list):
        if len(confidence_list) == 0:
            return False
            
        maxValue = confidence_list[0]
        for i in range(1, len(confidence_list)):
            if maxValue < confidence_list[i]:
                maxValue = confidence_list[i]

        if (maxValue * 100) >= 30:
        # 유사도 리스트 추가
            statement.set_confidence(maxValue * 100)
            # statement.set_confidence_list(maxValue * 100)
            return True
        else:
            return False

    from .comparisons import levenshtein_distance

    samples = logic['inputs_pos'].split('|')      
    confidence_check = []
    for sample in samples:
        sample = sample.replace(' ', '')
        confidence = levenshtein_distance(statement.input['pos'], sample)
        confidence_check.append(confidence)

        if len(confidence_check) == 5:
            if sum(confidence_check) / 5 <= 0.1:
                return False

    return max_confidence(confidence_check)


# def match_sentence(logic, statement):
#     def test(confidence_list, statement):
#         confidence = max(confidence_list)
#         if (confidence * 100) >= 60:
#             # 유사도 리스트 추가
#             statement.set_confidence_list((confidence * 100))
#             return True
#         return False
#     from .comparisons import levenshtein_distance

#     samples = logic['inputs_pos'].split('|')
#     # samples = logic['inputs'].split('|')
#     confidence_list = []
#     for sample in samples:
#         sample = sample.replace(' ', '')
#         # if sample == '[all]': return True
#         confidence = levenshtein_distance(statement.input['pos'], sample)
#         confidence_list.append(confidence)

#     return test(confidence_list, statement)




def match_keyword(logic, statement):
    samples = logic['inputs'].split('|')
    if logic['inputs_relation'] == 'OR':
        for sample in samples:
            sample = sample.replace(' ', '')
            # sample = replace_entity(statement, sample)
            if sample in statement.input['text']:
                # statement.set_confidence(95)
                return True
        return False
    else:
        for sample in samples:
            sample = sample.replace(' ', '')
            # sample = replace_entity(statement, sample)
            if sample not in statement.input['text']:
                return False
        return True


def match_corpus(logic, statement):
    samples = logic['inputs_pos'].split('|')
    if logic['inputs_relation'] == 'OR':
        for sample in samples:
            sample = sample.replace(' ', '')
            # sample = replace_entity(statement, sample)
            if sample in statement.input['pos']:
                return True
        return False
    else:
        for sample in samples:
            sample = sample.replace(' ', '')
            # sample = replace_entity(statement, sample)
            if sample not in statement.input['pos']:
                return False
        return True


def match_pos(logic, statement):
    samples = logic['inputs'].split('|')
    if logic['inputs_relation'] == 'OR':
        for sample in samples:
            sample = sample.replace(' ', '')
            # sample = replace_entity(statement, sample)
            for postag in statement.input['postag']:
                if sample in postag[1]:
                    return True
        return False
    else:
        for sample in samples:
            sample = sample.replace(' ', '')
            # sample = replace_entity(statement, sample)
            for postag in statement.input['postag']:
                if sample in postag[1]:
                    return False
        return True


def make_response(response, statement):
    import random
    if response['type'] in ('text', 'media', 'expression', 'command'):
        item = {}
        statement.result['intent_id'] = 0
        if response['type'] == 'text':
            _text = statement.cache_storage.random_cache_response(
                statement.get_cache_key(),
                response['outputs']
            )
            if _text.strip() == '_blank':
                return statement
            for _key, _value in statement.context['variables'].items():
                _text = _text.replace('{' + _key + '}', _value)
            item[response['type']] = _text
        else:
            item[response['type']] = random.choice(response['outputs'])

        # item['text'] = re.sub('[^a-z A-Z 가-힣 0-9 .,?!_]', '', response)
        statement.output.append(item)
        # if response['type'] == 'expression':
        #     statement.output.insert(0, item)
        # else:
        #     statement.output.append(item)

    elif response['type'] == 'custom':
        custom_function = statement.storage.get_custom_function_for_module(response['custom_module_id'])
        if custom_function is not None:
            intent = statement.storage.get_custom_intent_node_text(response['custom_module_intent_id'])
            if intent is not None:
                from chatterbot import utils
                adapter = utils.initialize_class('chatterbot.logic.' + custom_function['adapter'], statement.chatbot)
                adapter.id = custom_function['module_id']
                adapter.title = custom_function['module_text']
                adapter.process(statement, intent)

    return statement

def make_logic_response(response, logic_name, statement):

    item = {}
    item['text'] = re.sub('[^a-z A-Z 가-힣 0-9 .,?!_]', '', response)

    statement.output[0] = item

    statement.result['logic_property'] = logic_name

    return statement