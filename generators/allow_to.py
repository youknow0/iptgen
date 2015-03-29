from parsers.allow_to import AllowToRule
from generators.registry import register_generator
from hooks.registry import call_hook
from generators.addr import addr_generator
from os import linesep

class AllowToGenerator(object):

    def generate(self, rule):
        rule_str = "-A FORWARD "

        if rule.protocol == "tcp":
            rule_str += "-p tcp -m state --state NEW "
        elif rule.protocol == "udp":
            rule_str += "-p udp"
        else: 
            raise "Unknown proto"


        # generate one rule per addr of the host
        rule_out = ""
        for addr in addr_generator.addrs[rule.host]:
            myrule = rule_str + ("--dport %s -s %s -d %s" 
                                    % (rule.port, addr, rule.dest))
            myrule = call_hook("rule_allow_to", 
                                 myrule, rule)
            rule_out += myrule + linesep


        return rule_out
        rule_str += ("--dport %s -s %s -d %s" % 
                     (rule.port, rule.host, rule.dest))

        rule_str = call_hook("rule_allow_to", 
                             rule_str, rule)

        return rule_str

_gen = AllowToGenerator()
register_generator("allow_to", _gen.generate)

