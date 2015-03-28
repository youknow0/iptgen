from parsers.allow_in import allow_in_parser
from hooks.registry import call_hook
from generators.registry import register_generator

class AllowInGenerator(object):

    def generate(self, rule):
        rule_str = "-A FORWARD "

        if rule.protocol == "tcp":
            rule_str += "-p tcp -m state --state NEW "
        elif rule.protocol == "udp":
            rule_str += "-p udp "
        else: 
            raise "Unknown proto"

        rule_str += ("--dport %s -d %s" % (rule.port, rule.host))

        rule_str = call_hook("rule_allow_in", 
                             rule_str, rule)

        return rule_str


_gen = AllowInGenerator()
register_generator("allow_in", _gen.generate)
