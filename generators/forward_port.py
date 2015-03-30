from parsers.forward_port import ForwardPortRule
from generators.registry import register_generator
from generators.exception import GeneratorException
from hooks.registry import call_hook
from generators.addr import addr_generator
from socket import getservbyname

class ForwardPortGenerator(object):

    def _lookup_port(self, port):
        # is a digit, we assume this is a raw port number
        if port.isdigit():
            return port

        # otherwise, we perform a service lookup
        try:
            return getservbyname(port)
        except socket.error:
            raise GeneratorException('Unknown service "%s"' % (port,))

    def generate(self, rule):
        rule_str = "-A PREROUTING -j DNAT "

        if rule.protocol == "tcp":
            rule_str += "-p tcp "
        elif rule.protocol == "udp":
            rule_str += "-p udp"
        else: 
            raise "Unknown proto"

        if not rule.ip_to in addr_generator.addrs[rule.host]:
            raise GeneratorException('IP "%s" is not owned by host "%s"'
                                     % (rule.ip_to, rule.host))

        if rule.port.find(':') != -1:
            (port_start, port_end) = rule.port.split(':')
            port_start = self._lookup_port(port_start)
            port_end = self._lookup_port(port_end)
        
            port = '%s:%s' % (port_start, port_end)

            # for port ranges, iptables expects a minus in the --to 
            # argument, but a colon in the --dport argument...
            toport = port.replace(":", "-")
        else:
            port = self._lookup_port(rule.port)
            toport = port

        rule_str += ("--dport %s " % (port,))
        rule_str += ("-d %s " % (rule.ip_from,))
        rule_str += ("--to %s:%s " % (rule.ip_to, toport))

        rule_str = call_hook("rule_forward_port",
                             rule_str, rule)

        return rule_str

_gen = ForwardPortGenerator()
register_generator("forward_port", _gen.generate)

