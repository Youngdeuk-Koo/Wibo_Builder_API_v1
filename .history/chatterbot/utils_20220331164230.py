"""
ChatterBot utility functions
"""

def replace_entity(statement, _sample):
    for _k, _v in statement.input['entities'].items():
        if _k in _sample:
            _sample = _sample.replace(_k, _v)
    return _sample


def pos_tagging(statement):
    if 'text' in statement.input:
        import MeCab
        import sys
        import string
        import re

        enabled_pos_tag = [
            'NNG',
            'NNP',
            'NNB',
            'NNBC',
            'NR',
            'NP',

            'VV',
            'VA',
            'VX',
            'VCP',
            'VCN',
            'MM',

            'MAG',
            'MAJ',

            'IC',

            # 'JKS',
            # 'JKC',
            # 'JKG',
            # 'JKO',
            # 'JKB',
            # 'JKV',
            # 'JKQ',
            # 'JC',
            # 'JX',
            #
            # 'EP',
            # 'EF',
            # 'EC',
            # 'ETN',
            # 'ETM',

            'XPN',
            'XSN',
            'XSV',
            'XSA',

            'XR',

            # 'SF',
            # 'SE',
            # 'SSO',
            # 'SSC',
            # 'SC',
            # 'SY',

            'SH',
            'SL',
            'SN',
        ]

        t = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ko-dic')

        # #으로 시작 하면 무시
        # @들어가면 띄어쓰기 해서
        # []이부분은 제거했다가 다시 삽입

        text = statement.input['text']

        if text.startswith('#'):
            return text

        commands = []
        while (True):
            m = re.search(r'[[]\w+[]]', text)
            if m is None:
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

        text = ''.join(_w) + ''.join(commands)
        statement.input['pos'] = text

    return statement

def pos_tagging_str(text):
    import MeCab
    import sys
    import string
    import re

    enabled_pos_tag = [
        'NNG',
        'NNP',
        'NNB',
        'NNBC',
        'NR',
        'NP',

        'VV',
        'VA',
        'VX',
        'VCP',
        'VCN',
        'MM',

        'MAG',
        'MAJ',

        'IC',

        # 'JKS',
        # 'JKC',
        # 'JKG',
        # 'JKO',
        # 'JKB',
        # 'JKV',
        # 'JKQ',
        # 'JC',
        # 'JX',
        #
        # 'EP',
        # 'EF',
        # 'EC',
        # 'ETN',
        # 'ETM',

        'XPN',
        'XSN',
        'XSV',
        'XSA',

        'XR',

        # 'SF',
        # 'SE',
        # 'SSO',
        # 'SSC',
        # 'SC',
        # 'SY',

        'SH',
        'SL',
        'SN',
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
        if m is None:
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

    text = ''.join(_w) + ''.join(commands)

    return text


def import_module(dotted_path):
    """
    Imports the specified module based on the
    dot notated import path for the module.
    """
    import importlib

    module_parts = dotted_path.split('.')
    module_path = '.'.join(module_parts[:-1])
    module = importlib.import_module(module_path)

    return getattr(module, module_parts[-1])


def get_initialization_functions(obj, attribute):
    """
    Return all initialization methods for the comparison algorithm.
    Initialization methods must start with 'initialize_' and
    take no parameters.
    """
    initialization_methods = {}

    attribute_parts = attribute.split('.')
    outermost_attribute = getattr(obj, attribute_parts.pop(0))
    for next_attribute in attribute_parts:
        outermost_attribute = getattr(outermost_attribute, next_attribute)

    for method in dir(outermost_attribute):
        if method.startswith('initialize_'):
            initialization_methods[method] = getattr(outermost_attribute, method)

    return initialization_methods


def initialize_class(data, *args, **kwargs):
    """
    :param data: A string or dictionary containing a import_path attribute.
    """
    if isinstance(data, dict):
        import_path = data.get('import_path')
        data.update(kwargs)
        Class = import_module(import_path)

        return Class(*args, **data)
    else:
        Class = import_module(data)

        return Class(*args, **kwargs)


def validate_adapter_class(validate_class, adapter_class):
    """
    Raises an exception if validate_class is not a
    subclass of adapter_class.

    :param validate_class: The class to be validated.
    :type validate_class: class

    :param adapter_class: The class type to check against.
    :type adapter_class: class

    :raises: Adapter.InvalidAdapterTypeException
    """
    from chatterbot.adapters import Adapter

    # If a dictionary was passed in, check if it has an import_path attribute
    if isinstance(validate_class, dict):

        if 'import_path' not in validate_class:
            raise Adapter.InvalidAdapterTypeException(
                'The dictionary {} must contain a value for "import_path"'.format(
                    str(validate_class)
                )
            )

        # Set the class to the import path for the next check
        validate_class = validate_class.get('import_path')

    if not issubclass(import_module(validate_class), adapter_class):
        raise Adapter.InvalidAdapterTypeException(
            '{} must be a subclass of {}'.format(
                validate_class,
                adapter_class.__name__
            )
        )


def nltk_download_corpus(resource_path):
    """
    Download the specified NLTK corpus file
    unless it has already been downloaded.

    Returns True if the corpus needed to be downloaded.
    """
    from nltk.data import find
    from nltk import download
    from os.path import split, sep
    from zipfile import BadZipfile

    # Download the NLTK data only if it is not already downloaded
    _, corpus_name = split(resource_path)

    # From http://www.nltk.org/api/nltk.html
    # When using find() to locate a directory contained in a zipfile,
    # the resource name must end with the forward slash character.
    # Otherwise, find() will not locate the directory.
    #
    # Helps when resource_path=='sentiment/vader_lexicon''
    if not resource_path.endswith(sep):
        resource_path = resource_path + sep

    downloaded = False

    try:
        find(resource_path)
    except LookupError:
        download(corpus_name)
        downloaded = True
    except BadZipfile:
        raise BadZipfile(
            'The NLTK corpus file being opened is not a zipfile, '
            'or it has been corrupted and needs to be manually deleted.'
        )

    return downloaded


def treebank_to_wordnet(pos):
    """
    Convert Treebank part-of-speech tags to Wordnet part-of-speech tags.
    * https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    * http://www.nltk.org/_modules/nltk/corpus/reader/wordnet.html
    """
    data_map = {
        'N': wordnet.NOUN,
        'J': wordnet.ADJ,
        'V': wordnet.VERB,
        'R': wordnet.ADV
    }

    return data_map.get(pos[0])


def remove_stopwords(tokens, language):
    """
    Takes a language (i.e. 'english'), and a set of word tokens.
    Returns the tokenized text with any stopwords removed.
    Stop words are words like "is, the, a, ..."

    Be sure to download the required NLTK corpus before calling this function:
    - from chatterbot.utils import nltk_download_corpus
    - nltk_download_corpus('corpora/stopwords')
    """
    from nltk.corpus import stopwords

    # Get the stopwords for the specified language
    stop_words = stopwords.words(language)

    # Remove the stop words from the set of word tokens
    tokens = set(tokens) - set(stop_words)

    return tokens


def get_greatest_confidence(statement, options):
    """
    Returns the greatest confidence value for a statement that occurs
    multiple times in the set of options.

    :param statement: A statement object.
    :param options: A tuple in the format of (confidence, statement).
    """
    values = []
    for option in options:
        if option[1] == statement:
            values.append(option[0])

    return max(values)


def get_response_time(chatbot, statement='Hello'):
    """
    Returns the amount of time taken for a given
    chat bot to return a response.

    :param chatbot: A chat bot instance.
    :type chatbot: ChatBot

    :returns: The response time in seconds.
    :rtype: float
    """
    import time

    start_time = time.time()

    chatbot.get_response(statement)

    return time.time() - start_time


def print_progress_bar(description, iteration_counter, total_items, progress_bar_length=20):
    """
    Print progress bar
    :param description: Training description
    :type description: str

    :param iteration_counter: Incremental counter
    :type iteration_counter: int

    :param total_items: total number items
    :type total_items: int

    :param progress_bar_length: Progress bar length
    :type progress_bar_length: int

    :returns: void
    :rtype: void
    """
    import sys

    percent = float(iteration_counter) / total_items
    hashes = '#' * int(round(percent * progress_bar_length))
    spaces = ' ' * (progress_bar_length - len(hashes))
    sys.stdout.write("\r{0}: [{1}] {2}%".format(description, hashes + spaces, int(round(percent * 100))))
    sys.stdout.flush()
    if total_items == iteration_counter:
        print("\r")
