from hooks.registry import register_hook

## Parsers to load
# the host parser should probably never be removed
from parsers.host import HostParser
from parsers.forward_port import ForwardPortParser

# this time, we load the other parsers...
from parsers.allow_in import AllowInParser
from parsers.allow_out import AllowOutParser

## Generators to load
from generators.host import HostGenerator
from generators.forward_port import ForwardPortGenerator
# ...but we register the dummy generator for them.
from generators.dummy import DummyGenerator
dummy = DummyGenerator()
from generators.registry import register_generator
register_generator("allow_in", dummy.generate)
register_generator("allow_out", dummy.generate)


## example hooks
# add a interface for forward_port
register_hook("rule_forward_port", lambda value, params:
              value + " -i ppp0")
