from parsers.allow_out import AllowOutRule
from generators.registry import register_generator
from hooks.registry import call_hook

class AllowOutGenerator(object):

    def generate(self, rule):
        rule_str = "-A FORWARD "

        if rule.protocol == "tcp":
            rule_str += "-p tcp -m state --state NEW "
        elif rule.protocol == "udp":
            rule_str += "-p udp"
        else: 
            raise "Unknown proto"

        rule_str += ("--dport %s -s %s" % (rule.port, rule.host))

        rule_str = call_hook("rule_allow_out", 
                             rule_str, rule)

        return rule_str

_gen = AllowOutGenerator()
register_generator("allow_out", _gen.generate)

