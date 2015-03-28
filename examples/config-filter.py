from hooks.registry import register_hook

## Parsers to load
# the host parser should probably never be removed
from parsers.host import HostParser
from parsers.allow_in import AllowInParser
from parsers.allow_out import AllowOutParser
# the forward_port parser is loaded...
from parsers.forward_port import ForwardPortParser

## Generators to load
from generators.host import HostGenerator
from generators.allow_in import AllowInGenerator
from generators.allow_out import AllowOutGenerator
# ...but the DummyGenerator is associated to it, thus forward_port
# rules are ignored when this config is used.
from generators.dummy import DummyGenerator
dummy = DummyGenerator()
from generators.registry import register_generator
register_generator("forward_port", dummy.generate)


## example hooks
# physdev hook for allow_out
register_hook("rule_allow_out", lambda value, params: 
              value + " -m physdev --physdev-in vif-%s" % (params.host,))

# physdev hook for allow_in
register_hook("rule_allow_in", lambda value, params: 
              value + " -m physdev --physdev-out vif-%s" % (params.host,))
