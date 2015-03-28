_generators = {}

def register_generator(keyword, handler):
    _generators[keyword] = handler

def get_generator(keyword):
    return _generators[keyword]

