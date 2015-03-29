from parsers.forward_port import ForwardPortRule
from generators.registry import register_generator
from hooks.registry import call_hook

class ForwardPortGenerator(object):

    def generate(self, rule):
        rule_str = "-A PREROUTING -j DNAT "

        if rule.protocol == "tcp":
            rule_str += "-p tcp "
        elif rule.protocol == "udp":
            rule_str += "-p udp"
        else: 
            raise "Unknown proto"

        # for port ranges, iptables expects a minus in the --to 
        # argument, but a colon in the --dport argument...
        toport = rule.port.replace(":", "-")

        rule_str += ("--dport %s " % (rule.port,))
        rule_str += ("--to %s:%s " % (rule.host, toport))

        rule_str = call_hook("rule_forward_port",
                             rule_str, rule)

        return rule_str

_gen = ForwardPortGenerator()
register_generator("forward_port", _gen.generate)

