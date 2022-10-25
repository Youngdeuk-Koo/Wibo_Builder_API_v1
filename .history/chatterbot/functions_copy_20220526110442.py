import torch


device = torch.device("cpu")
model = torch.load("SAVE_MODEL_DIR/model", map_location=device)



# True가 나올때 까지 데이터베이스 검색
def recognize_intent(next_node, statement):
    
    # import time
    # start = time.time()
    
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
            # end = time.time()
            # time = end - start
            return True
        
    return False


# def match_sentence(logic, statement):
#     from .comparisons_copy import levenshtein_distance
    
#     samples = logic['inputs'].split('|')
#     embeddings = logic['embedding']
    
#     sample_embedding = model.encode(statement.input['text'])
    
#     for sample, db_embedding in zip(samples, embeddings):
#         if sample == '[all]': 
#             return True        
        
#         confidence = levenshtein_distance(db_embedding, sample_embedding)
#         if (confidence * 100) >= logic['sim_threshold']:

#             return True
        
#     return False   

def match_sentence(logic, statement):
    from .comparisons_copy import levenshtein_distance_check
    
    samples = logic['inputs_pos'].split('|')
    
    for sample in samples:
        sample = sample.replace(' ', '')
        if sample == '[all]': return True
        # sample = replace_entity(statement, sample)
        confidence = levenshtein_distance_check(statement.input['pos'], sample)
        # if (confidence * 100) >= logic['sim_threshold'] - 20:
        if (confidence * 100) >= 60:
            return True
    return False

def match_keyword(logic, statement):
    samples = logic['inputs'].split('|')
    if logic['inputs_relation'] == 'OR':
        for sample in samples:
            if sample in statement.input['text']:
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






