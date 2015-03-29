from parsers.exception import ParserException

_parsers = {}

def register_parser(keyword, handler):
    if keyword in _parsers:
        raise "Attempt to register duplicate keyword %s!" % (keyword,)

    _parsers[keyword] = handler

def get_parser(keyword):
    try:
        return _parsers[keyword]
    except KeyError as e:
        raise ParserException('Unknown keyword "%s"' % (keyword,))


