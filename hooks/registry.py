_hooks = {}

def register_hook(name, hook_func):
    if not name in _hooks:
        _hooks[name] = []

    _hooks[name].append(hook_func)

def call_hook(name, value, args):
    if name in _hooks:
        for hook in _hooks[name]:
            value = hook(value, args)

    return value

