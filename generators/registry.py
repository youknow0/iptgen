from generators.exception import GeneratorException

_generators = {}

def register_generator(keyword, handler):
    _generators[keyword] = handler

def get_generator(keyword):
    try:
        return _generators[keyword]
    except KeyError:
        raise GeneratorException('No generator registered for keyword "%s"' % (keyword,))

