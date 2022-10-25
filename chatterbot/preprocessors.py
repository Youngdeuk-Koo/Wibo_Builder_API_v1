"""
Statement pre-processors.
"""

def pos_tagging(statement):
    if 'text' in statement.input:
        text = statement.input['text']
        if text == '':
            statement.input['pos'] = ''
            return statement

        # if 'entities' in statement.input:
        #     for _k, _v in statement.input['entities'].items():
        #         if text != '' and _v != '':
        #             if _v in text:
        #                 text = text.replace(_v, _k)

        import MeCab
        import re

        enabled_pos_tag = [
            'NNG','NNP','NNB','NNBC','NR','NP',
            'VV','VA','VX','VCP','VCN','MM',
            'MAG','MAJ',
            'IC',
            # 'JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ', 'JC', 'JX',
            # 'EP', 'EF', 'EC', 'ETN', 'ETM',
            'XPN', 'XSN', 'XSV', 'XSA', 'XR',
            # 'SF', 'SE', 'SSO', 'SSC', 'SC', 'SY',
            'SH', 'SL', 'SN',
        ]

        t = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ko-dic')

        # #으로 시작 하면 무시
        # @들어가면 띄어쓰기 해서
        # []이부분은 제거했다가 다시 삽입

        if text.startswith('#'):
            return text

        commands = []
        while (True):
            m = re.search(r'[[]\w+[]]', text)
            if m == None:
                break
            commands.append(text[m.start(): m.end()])
            text = text[:m.start()] + text[m.end():]

        words = text.split(' ')

        _w = []
        for word in words:
            if word.startswith('@'):
                _w.append(word)
            else:
                t.parse(word)
                m = t.parseToNode(word)
                while m:
                    # print(m.surface, "\t", m.feature)
                    pos = m.feature.split(',')
                    if '+' in pos[0]:
                        for _f in pos[7].split('+'):
                            __f = _f.split('/')
                            if __f[1] in enabled_pos_tag:
                                _w.append(__f[0])
                    else:
                        if pos[0] in enabled_pos_tag:
                            _w.append(m.surface)
                    m = m.next

        text = ' '.join(_w) + ''.join(commands)

        # if 'entities' in statement.input:
        #     for _k, _v in statement.input['entities'].items():
        #         if _k in text:
        #             text = text.replace(_k, _v)

        statement.input['pos'] = text

        from konlpy.tag import Mecab
        mecab = Mecab()
        statement.input['postag'] = mecab.pos(statement.input['text'])

    return statement

def recognize_entity(statement):
    statement.input['entities'] = {}
    _input = statement.input['text']
    if _input == '':
        return statement

    from .comparisons import levenshtein_distance

    def window(fseq, window_size=5):
        for i in range(len(fseq) - window_size + 1):
            start = i
            end = i + window_size
            yield fseq[start:end]

    entities = statement.storage.get_entities(statement.chatbot.chatbot_id)

    for entity in entities:
        _entity_items = entity['dataset'].split(',')
        statement.input['entities']['@' + entity['text']] = ''
        _confidence = 0
        _threshold = 0.7
        for _item in _entity_items:
            _tmp_item = _item.replace(' ','')

            for _seq in window(_input, len(_tmp_item)):
                _confidence = levenshtein_distance(_tmp_item, _seq)
                if _confidence > _threshold:
                    statement.input['entities']['@' + entity['text']] = _item.strip()
            if _confidence > _threshold:
                break

    statement.input['text'] = _input

    return statement

def remove_blank(statement):
    # statement.input['text'] = statement.input['text'].replace(' ', '')
    # statement.input['pos'] = statement.input['pos'].replace(' ', '')
    return statement



# def genearte_ngram(statement, ngram_range=(1,2)):
#     if 'text' in statement.input:
#         from sklearn.feature_extraction.text import CountVectorizer
#         from nltk.tokenize import TreebankWordTokenizer
#         string = statement.input['text']
#         vect = CountVectorizer(ngram_range=ngram_range, tokenizer=TreebankWordTokenizer().tokenize)
#         analyzer = vect.build_analyzer()
#         statement.input['ngrams'] = analyzer(string)
#
#     return statement