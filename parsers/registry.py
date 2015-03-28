_parsers = {}

def register_parser(keyword, handler):
    if keyword in _parsers:
        raise "Attempt to register duplicate keyword %s!" % (keyword,)

    _parsers[keyword] = handler

def get_parser(keyword):
    return _parsers[keyword]


