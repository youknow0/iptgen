from parsers.allow_out import AllowOutRule
from generators.registry import register_generator
from hooks.registry import call_hook
from generators.addr import addr_generator
from os import linesep

class AllowOutGenerator(object):

    def generate(self, rule):
        rule_str = "-A FORWARD -j ACCEPT "

        if rule.protocol == "tcp":
            rule_str += "-p tcp -m state --state NEW "
        elif rule.protocol == "udp":
            rule_str += "-p udp"
        else: 
            raise "Unknown proto"


        # generate one rule per addr of the host
        rule_out = ""
        for addr in addr_generator.addrs[rule.host]:
            myrule = rule_str + ("--dport %s -s %s" 
                                    % (rule.port, addr))
            myrule = call_hook("rule_allow_out", 
                                 myrule, rule)
            rule_out += myrule + linesep

        return rule_out

_gen = AllowOutGenerator()
register_generator("allow_out", _gen.generate)

