from parsers.allow_to import AllowToRule
from generators.registry import register_generator
from hooks.registry import call_hook

class AllowToGenerator(object):

    def generate(self, rule):
        rule_str = "-A FORWARD "

        if rule.protocol == "tcp":
            rule_str += "-p tcp -m state --state NEW "
        elif rule.protocol == "udp":
            rule_str += "-p udp"
        else: 
            raise "Unknown proto"

        rule_str += ("--dport %s -s %s -d %s" % 
                     (rule.port, rule.host, rule.dest))

        rule_str = call_hook("rule_allow_tovm", 
                             rule_str, rule)

        return rule_str

_gen = AllowToGenerator()
register_generator("allow_to", _gen.generate)

