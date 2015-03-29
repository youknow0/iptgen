from parsers.exception import ParserException
from parsers.registry import register_parser
from collections import namedtuple
from parsers.host import host_parser

ForwardPortRule = namedtuple("ForwardPortRule", "host port protocol ip")

"""
syntax:
    forward_port <ip to forward to> <port  to forward> [proto]
"""

class ForwardPortParser(object):

    def parse(self, tokens):
        host = host_parser.current_host 
        if host == None:
            raise ParserException(
                "ForwardPort must be inside Host section!")

        if len(tokens) < 3:
            raise ParserException(
                "ForwardPort keyword requires two arguments!")

        ip = tokens[1]
        port = tokens[2]

        # optional protocol argument
        if 3 in tokens:
            proto = tokens[3]
            if proto != "udp" and proto != "tcp":
                raise ParserException("Unknown protocol %s" % (proto,))
        else:
            proto = "tcp"

        rule = ForwardPortRule(
            port=port, protocol=proto, host=host, ip=ip)

        return rule

forward_port_parser = ForwardPortParser()
register_parser("forward_port", forward_port_parser.parse)

